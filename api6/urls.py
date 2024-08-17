from django.urls import path
from .views import (
    RegisterAPIView,
    LoginAPIView,
    LogoutAPIView,
    ProfileAPIView,
    PasswordResetRequestAPIView,
    PasswordResetConfirmAPIView,
    PasswordResetCompleteAPIView
)

urlpatterns = [
    path('register/', RegisterAPIView.as_view(), name='api_register'),
    path('login/', LoginAPIView.as_view(), name='api_login'),
    path('logout/', LogoutAPIView.as_view(), name='api_logout'),
    path('profile/', ProfileAPIView.as_view(), name='api_profile'),
    path('password-reset/', PasswordResetRequestAPIView.as_view(), name='api_password_reset_request'),
    path('password-reset-confirm/<uidb64>/<token>/', PasswordResetConfirmAPIView.as_view(), name='api_password_reset_confirm'),
    path('password-reset-complete/', PasswordResetCompleteAPIView.as_view(), name='api_password_reset_complete'),
]
