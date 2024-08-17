from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework import viewsets
from django.shortcuts import get_object_or_404
from patients.models import Appointment
from .serializers import AppointmentSerializer, ContactSerializer
from chat.models import ChatRoom, Message, PrivateMessage
from api2.serializers import MessageSerializer, PrivateMessageSerializer, ChatRoomSerializer
from contact.models import Contact
from django.contrib.auth import get_user_model
from api6.serializers import CustomUserChangeSerializer
User = get_user_model()

class PatientChatRoomListView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        chat_rooms = ChatRoom.objects.filter(users=request.user)
        serializer = ChatRoomSerializer(chat_rooms, many=True)
        return Response(serializer.data)

class PatientChatRoomDetailView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, pk):
        chat_room = get_object_or_404(ChatRoom, pk=pk)
        messages = Message.objects.filter(chat_room=chat_room).order_by("timestamp")
        message_serializer = MessageSerializer(messages, many=True)
        return Response({
            'chat_room': ChatRoomSerializer(chat_room).data,
            'messages': message_serializer.data
        })

    def post(self, request, pk):
        chat_room = get_object_or_404(ChatRoom, pk=pk)
        serializer = MessageSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user, chat_room=chat_room)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class PatientPrivateMessageListView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        users = User.objects.exclude(username=request.user.username)
        serializer = CustomUserChangeSerializer(users, many=True)
        return Response(serializer.data)

class PatientPrivateMessageDetailView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, username):
        recipient = get_object_or_404(User, username=username)
        messages = PrivateMessage.objects.filter(
            sender=request.user, recipient=recipient
        ) | PrivateMessage.objects.filter(
            sender=recipient, recipient=request.user
        ).order_by("timestamp")
        serializer = PrivateMessageSerializer(messages, many=True)
        return Response({
            'recipient': CustomUserChangeSerializer(recipient).data,
            'messages': serializer.data
        })

    def post(self, request, username):
        recipient = get_object_or_404(User, username=username)
        serializer = PrivateMessageSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(sender=request.user, recipient=recipient)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class PatientAppointmentsView(ListCreateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = AppointmentSerializer

    def get_queryset(self):
        return Appointment.objects.filter(patient=self.request.user)

    def perform_create(self, serializer):
        serializer.save(patient=self.request.user, status='scheduled', nurse=None)

class UpdateAppointmentStatusView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, pk):
        status = request.data.get("status")
        appointment = get_object_or_404(Appointment, pk=pk)
        if request.user.role == "patient" and appointment.patient == request.user:
            if status in ["completed", "canceled"]:
                appointment.status = status
                appointment.save()
                return Response({'status': 'updated'}, status=status.HTTP_200_OK)
            return Response({'error': 'Invalid status'}, status=status.HTTP_400_BAD_REQUEST)
        return Response({'error': 'Unauthorized'}, status=status.HTTP_403_FORBIDDEN)

class PatientContactView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        if request.user.role.lower() != "patient":
            return Response({'error': 'Not authorized'}, status=status.HTTP_403_FORBIDDEN)

        serializer = ContactSerializer(data=request.data)
        if serializer.is_valid():
            contact = serializer.save(user=request.user)
            recipient_role = serializer.validated_data.get("recipient_role")
            if recipient_role == "doctor":
                contact.recipient = User.objects.filter(role="doctor").first()
            elif recipient_role == "patient":
                contact.recipient = request.user
            if contact.recipient is None:
                return Response({'error': 'No recipient found'}, status=status.HTTP_400_BAD_REQUEST)
            contact.save()
            return Response(ContactSerializer(contact).data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class PatientMessagesView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        if request.user.role.lower() != "patient":
            return Response({'error': 'Not authorized'}, status=status.HTTP_403_FORBIDDEN)
        messages = Contact.objects.filter(recipient_role="doctor", user=request.user)
        serializer = ContactSerializer(messages, many=True)
        return Response(serializer.data)
