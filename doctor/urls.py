from django.urls import path
from . import views

app_name = "doctor"

urlpatterns = [
    path("doctor_appointments/", views.doctor_appointments, name="doctor_appointments"),
    path(
        "doctor_appointments/<int:pk>/status/",
        views.update_appointment_status,
        name="update_appointment_status",
    ),
    path("static-file-debug/", views.static_file_debug, name="static_file_debug"),
    path("contact/patient/", views.doctor_contact, name="doctor_contact"),
    path("messages/", views.doctor_messages, name="doctor_messages"),
]
