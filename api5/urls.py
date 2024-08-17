from django.urls import path
from . import views

urlpatterns = [
    path('chat/rooms/', views.PatientChatRoomListView.as_view(), name='api_patient_chat_room_list'),
    path('chat/rooms/<int:pk>/', views.PatientChatRoomDetailView.as_view(), name='api_patient_chat_room_detail'),
    path('chat/private-messages/', views.PatientPrivateMessageListView.as_view(), name='api_patient_private_message_list'),
    path('chat/private-messages/<str:username>/', views.PatientPrivateMessageDetailView.as_view(), name='api_patient_private_message_detail'),
    path('appointments/', views.PatientAppointmentsView.as_view(), name='api_patient_appointments'),
    path('appointments/<int:pk>/status/', views.UpdateAppointmentStatusView.as_view(), name='api_update_appointment_status'),
    path('contact/', views.PatientContactView.as_view(), name='api_patient_contact'),
    path('messages/', views.PatientMessagesView.as_view(), name='api_patient_messages'),
]
