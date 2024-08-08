from django.contrib import admin
from .models import DoctorProfile, DoctorAppointment, DoctorMedicalRecord


@admin.register(DoctorProfile)
class DoctorProfileAdmin(admin.ModelAdmin):
    list_display = ("user", "specialty", "department", "phone_number")
    search_fields = ("user__username", "specialty", "department")


@admin.register(DoctorAppointment)
class DoctorAppointmentAdmin(admin.ModelAdmin):
    list_display = ("patient", "date", "reason", "status")
    list_filter = ("status", "date")
    search_fields = ("patient__username", "reason")


@admin.register(DoctorMedicalRecord)
class DoctorMedicalRecordAdmin(admin.ModelAdmin):
    list_display = ("patient", "date", "diagnosis", "treatment")
    search_fields = ("patient__username", "diagnosis", "treatment")
    list_filter = ("date",)
