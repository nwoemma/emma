from rest_framework import serializers
from doctor.models import DoctorAppointment
from contact.models import Contact
from patients.models import Appointment

class DoctorAppointmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = DoctorAppointment
        fields = ['id', 'doctor', 'date', 'status']  # Adjust fields based on your model

class ContactSerializer(serializers.ModelSerializer):
    class Meta:
        model = Contact
        fields = ['id', 'user', 'recipient', 'recipient_role', 'message', 'created_at']  # Adjust fields based on your model
