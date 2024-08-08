from django.urls import path
from . import views

app_name = "doctor"

urlpatterns = [
    path("appointments/", views.doctor_appointments, name="doctor_appointments"),
    path(
        "appointments/<int:pk>/status/<str:status>/",
        views.update_appointment_status,
        name="update_appointment_status",
    ),
]
