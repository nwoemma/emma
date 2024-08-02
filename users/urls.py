from django.urls import path
from django.contrib.auth import views as auth_views
from . import views
from .views import RegisterAPIView, LoginAPIView, LogoutAPIView


app_name = "users"

urlpatterns = [
    path('register/', views.register, name='register'),
    path('register/', views.RegisterAPIView.as_view(), name='register'),
    path('login/', views.loginUser, name='loginUser'),
    path('logout/', views.logoutUser, name='logoutUser'),
    path('password_reset/', auth_views.PasswordResetView.as_view(
        template_name='users/password_reset.html',
        email_template_name='users/password_reset_email.html',
        subject_template_name='users/password_reset_subject.txt',
        success_url='/password_reset/done/'  # Redirects here after email sent
    ), name='password_reset'),
    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(
        template_name='users/password_reset_done.html'
    ), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(
        template_name='users/password_reset_confirm.html',
        success_url='/password_reset_complete/'  # Redirects here after password reset
    ), name='password_reset_confirm'),
    path('password_reset_complete/', auth_views.PasswordResetCompleteView.as_view(
        template_name='users/password_reset_complete.html'
    ), name='password_reset_complete'),
    path('registerAPI/', RegisterAPIView.as_view(), name='register'),
    path('loginAPI/', LoginAPIView.as_view(), name='login'),
    path('logoutAPI/', LogoutAPIView.as_view(), name='logout'),
]
