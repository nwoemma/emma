from django.db import models
from accounts.models import CustomUser
from django.utils import timezone


class DoctorProfile(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    is_active = models.BooleanField(default=True)
    department = models.CharField(max_length=100, default="General")
    specialty = models.CharField(max_length=100, default=None)
    phone_number = models.CharField(max_length=15, default=None)
    profile_picture = models.ImageField(
        upload_to="profile_pics/", blank=True, null=True
    )

    def __str__(self):
        return f"Doctor {self.user.username} - {self.specialty}"


class DoctorAppointment(models.Model):
    STATUS_CHOICES = [
        ("scheduled", "Scheduled"),
        ("pending", "Pending"),
        ("completed", "Completed"),
        ("canceled", "Canceled"),
    ]

    doctor = models.ForeignKey(
        CustomUser, on_delete=models.CASCADE, related_name="doctor_appointments_set"
    )
    patient = models.ForeignKey(
        CustomUser, on_delete=models.CASCADE, related_name="doctor_patient_appointment"
    )
    date = models.DateTimeField(default=timezone.now)
    reason = models.TextField()
    status = models.CharField(
        max_length=20, choices=STATUS_CHOICES, default="scheduled"
    )

    def __str__(self):
        return f"Appointment with {self.patient.username} on {self.date}"

    def __str__(self):
        return f"Appointment with {self.patient.username} on {self.date}"

    def save(self, *args, **kwargs):
        if self.pk:
            old_status = DoctorAppointment.objects.get(pk=self.pk).status
            if old_status != self.status:
                print(f"Status changed from {old_status} to {self.status}")

        super().save(*args, **kwargs)


class DoctorMedicalRecord(models.Model):
    doctor = models.OneToOneField(
        CustomUser, on_delete=models.CASCADE, related_name="doctor_medical_records"
    )
    patient = models.ForeignKey(
        CustomUser, on_delete=models.CASCADE, related_name="patient_medical_records"
    )
    date = models.DateTimeField(default=timezone.now)
    diagnosis = models.TextField()
    treatment = models.TextField()
    notes = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"Medical record for {self.patient.username} by Dr. {self.doctor.username} on {self.date}"
