from django.db import models
from accounts.models import CustomUser


class DoctorProfile(models.Model):
    user = models.OneToOneField(
        CustomUser, on_delete=models.CASCADE, related_name="doctor_profile"
    )
    department = models.CharField(max_length=100, blank=True, null=True)
    specialty = models.CharField(max_length=100, blank=True, null=True)
    phone_number = models.CharField(max_length=15, blank=True, null=True)
    profile_picture = models.ImageField(upload_to="doctor_pics/", blank=True, null=True)

    def __str__(self):
        return f"Doctor {self.user.username} - {self.specialty}"


class DoctorAppointment(models.Model):
    doctor = models.OneToOneField(
        CustomUser, on_delete=models.CASCADE, related_name="doctor_appointments"
    )
    patient = models.ForeignKey(
        CustomUser, on_delete=models.CASCADE, related_name="patient_appointments"
    )
    date = models.DateTimeField()
    reason = models.TextField()
    status = models.CharField(
        max_length=20,
        choices=[
            ("scheduled", "Scheduled"),
            ("completed", "Completed"),
            ("canceled", "Canceled"),
        ],
        default="scheduled",
    )

    def __str__(self):
        return f"Appointment with {self.patient.username} on {self.date}"


class DoctorMedicalRecord(models.Model):
    doctor = models.OneToOneField(
        CustomUser, on_delete=models.CASCADE, related_name="doctor_medical_records"
    )
    patient = models.ForeignKey(
        CustomUser, on_delete=models.CASCADE, related_name="patient_medical_records"
    )
    date = models.DateTimeField(auto_now_add=True)
    diagnosis = models.TextField()
    treatment = models.TextField()
    notes = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"Medical record for {self.patient.username} by Dr. {self.doctor.username} on {self.date}"
