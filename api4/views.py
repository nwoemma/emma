from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import api_view, permission_classes
from rest_framework.exceptions import ValidationError
from django.shortcuts import get_object_or_404
from doctor.models import DoctorAppointment
from patients.models import Appointment
from contact.models import Contact
from .serializers import DoctorAppointmentSerializer, ContactSerializer
from django.contrib.auth import get_user_model
import os
from django.conf import settings


User = get_user_model()

class DoctorAppointmentsView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        if request.user.role.lower() not in ["doctor"]:
            return Response({'detail': 'Not authorized'}, status=status.HTTP_403_FORBIDDEN)
        
        appointments = DoctorAppointment.objects.filter(doctor=request.user).order_by("-date")
        patient_appointments = Appointment.objects.filter(doctor=request.user)

        # Add flags to indicate whether the status allows for editing
        for appointment in patient_appointments:
            appointment.can_edit = appointment.status not in ["completed", "canceled"]

        appointment_serializer = DoctorAppointmentSerializer(appointments, many=True)
        patient_appointment_serializer = DoctorAppointmentSerializer(patient_appointments, many=True)

        return Response({
            'appointments': appointment_serializer.data,
            'patient_appointments': patient_appointment_serializer.data,
        }, status=status.HTTP_200_OK)


class UpdateAppointmentStatusView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, pk):
        if request.user.role.lower() not in ["doctor"]:
            return Response({'detail': 'Not authorized'}, status=status.HTTP_403_FORBIDDEN)

        appointment = get_object_or_404(DoctorAppointment, pk=pk, doctor=request.user)
        status = request.data.get("status")

        if status in ["completed", "canceled"]:
            appointment.status = status
            appointment.save()
            return Response({'message': f'Appointment status updated to {status}.'}, status=status.HTTP_200_OK)
        else:
            return Response({'error': 'Invalid status.'}, status=status.HTTP_400_BAD_REQUEST)


class StaticFileDebugView(APIView):
    def get(self, request):
        try:
            with open(
                os.path.join(settings.BASE_DIR, "static", "icon", "favicon.ico"), "rb"
            ) as f:
                return Response(f.read(), content_type="image/x-icon")
        except FileNotFoundError:
            return Response({'detail': 'File not found'}, status=status.HTTP_404_NOT_FOUND)


class DoctorContactView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        if request.user.role.lower() != "doctor":
            return Response({'detail': 'Not authorized'}, status=status.HTTP_403_FORBIDDEN)

        serializer = ContactSerializer(data=request.data)
        if serializer.is_valid():
            contact = serializer.save(user=request.user, recipient_role="doctor")
            
            recipient_role = serializer.validated_data.get("recipient_role")
            if recipient_role == "doctor":
                contact.recipient = User.objects.filter(role='doctor').first()
            elif recipient_role == "patient":
                contact.recipient = User.objects.filter(role='patient').first()

            if contact.recipient is None:
                return Response({'error': 'No recipient found based on the recipient role.'}, status=status.HTTP_400_BAD_REQUEST)

            contact.save()
            return Response({'message': 'Contact message sent.'}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class DoctorMessagesView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        if request.user.role.lower() not in ["doctor"]:
            return Response({'detail': 'Not authorized'}, status=status.HTTP_403_FORBIDDEN)

        messages = Contact.objects.filter(recipient_role="patient", user=request.user)
        serializer = ContactSerializer(messages, many=True)
        return Response({'messages': serializer.data}, status=status.HTTP_200_OK)
