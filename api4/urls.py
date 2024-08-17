from django.urls import path
from .views import DoctorAppointmentsView, UpdateAppointmentStatusView, StaticFileDebugView, DoctorContactView, DoctorMessagesView

urlpatterns = [
    path('appointments/', DoctorAppointmentsView.as_view(), name='api_doctor_appointments'),
    path('appointments/update/<int:pk>/', UpdateAppointmentStatusView.as_view(), name='api_update_appointment_status'),
    path('static/favicon/', StaticFileDebugView.as_view(), name='api_static_file_debug'),
    path('contact/', DoctorContactView.as_view(), name='api_doctor_contact'),
    path('messages/', DoctorMessagesView.as_view(), name='api_doctor_messages'),
]
