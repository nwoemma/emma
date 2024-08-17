from django.urls import path
from . import views

app_name = "patients"

urlpatterns = [
    path("chat/", views.patient_chat_room_list, name="patient_chat_room_list"),
    path(
        "chat/room/<int:pk>/",
        views.patient_chat_room_detail,
        name="patient_chat_room_detail",
    ),
    path(
        "chat/private/",
        views.patient_private_message_list,
        name="patient_private_message_list",
    ),
    path(
        "chat/private/<str:username>/",
        views.patient_private_message_detail,
        name="patient_private_message_detail",
    ),
    path("appointments/", views.patient_appointments, name="patient_appointments"),
    # URL for updating appointment status
    path(
        "appointments/update/<int:pk>/<str:status>/",
        views.update_appointment_status,
        name="update_appointment_status",
    ),
    path("contact/", views.patient_contact, name="patient_contact"),
    path("messages/", views.patient_messages, name="patient_messages"),
]
