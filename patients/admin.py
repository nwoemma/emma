from django.contrib import admin
from .models import PatientProfile, Appointment


@admin.register(PatientProfile)
class PatientProfileAdmin(admin.ModelAdmin):
    list_display = (
        "user",
        "address",
        "medical_history",
        "allergies",
        "emergency_contact",
        "insurance_details",
    )
    search_fields = (
        "user__username",
        "address",
        "medical_history",
        "allergies",
        "emergency_contact",
        "insurance_details",
    )


@admin.register(Appointment)
class AppointmentAdmin(admin.ModelAdmin):
    list_display = ("patient", "nurse", "date", "reason", "status")
    list_filter = ("status", "date")
    search_fields = ("patient__username", "nurse__username", "reason", "status")
