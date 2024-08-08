# patients/models.py
from django.db import models
from accounts.models import CustomUser


class PatientProfile(models.Model):
    user = models.OneToOneField(
        CustomUser, on_delete=models.CASCADE, related_name="patient_profile"
    )
    address = models.CharField(max_length=255, blank=True, null=True)
    medical_history = models.TextField(blank=True, null=True)
    allergies = models.TextField(blank=True, null=True)
    emergency_contact = models.CharField(max_length=100, blank=True, null=True)
    insurance_details = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return self.user.username


class Appointment(models.Model):
    STATUS_CHOICES = [
        ("scheduled", "Scheduled"),
        ("completed", "Completed"),
        ("canceled", "Canceled"),
    ]

    patient = models.ForeignKey(
        CustomUser, on_delete=models.CASCADE, related_name="appointments"
    )
    nurse = models.ForeignKey(
        CustomUser,
        on_delete=models.SET_NULL,
        related_name="nurse_appointments",
        null=True,
        blank=True,  # Allow nurse to be NULL
    )
    date = models.DateTimeField()
    reason = models.TextField()
    status = models.CharField(
        max_length=20, choices=STATUS_CHOICES, default="scheduled"
    )

    def __str__(self):
        return f"Appointment with {self.patient.username} on {self.date}"
