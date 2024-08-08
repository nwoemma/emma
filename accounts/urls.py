from django.urls import path
from accounts import views
from .forms import CustomPasswordResetForm, CustomSetPasswordForm

app_name = "accounts"

urlpatterns = [
    path("register/", views.register, name="register"),
    path("login/", views.loginUser, name="loginAccount"),
    path("logout/", views.logoutUser, name="logoutAccount"),
    path("profile/", views.profile, name="profile"),
    path("profile/edit/", views.edit_profile, name="edit_profile"),
    # Password Reset URLs
    path("password_reset/", views.password_reset_request, name="password_reset"),
    path("password_reset_done/", views.password_reset_done, name="password_reset_done"),
    path(
        "reset/<uidb64>/<token>/",
        views.password_reset_confirm,
        name="password_reset_confirm",
    ),
    path(
        "password_reset_complete/",
        views.password_reset_complete,
        name="password_reset_complete",
    ),
]
