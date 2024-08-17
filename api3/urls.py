from django.urls import path
from .views import RegisterView, LoginView, LogoutView, ProfileView, PasswordResetRequestView, PasswordResetConfirmView, PasswordResetCompleteView

urlpatterns = [
    path('register/', RegisterView.as_view(), name='api_register'),
    path('login/', LoginView.as_view(), name='api_login'),
    path('logout/', LogoutView.as_view(), name='api_logout'),
    path('profile/', ProfileView.as_view(), name='api_profile'),
    path('password_reset/', PasswordResetRequestView.as_view(), name='api_password_reset_request'),
    path('password_reset_confirm/<uidb64>/<token>/', PasswordResetConfirmView.as_view(), name='api_password_reset_confirm'),
    path('password_reset_complete/', PasswordResetCompleteView.as_view(), name='api_password_reset_complete'),
]
