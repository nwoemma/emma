from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import (
    CustomUserCreationForm,
    CustomAuthenticationForm,
    CustomUserChangeForm,
)
from .forms import CustomPasswordResetForm, CustomSetPasswordForm
from django.contrib.auth.views import PasswordResetView, PasswordResetConfirmView
from django.contrib.auth.forms import PasswordResetForm
from django.urls import reverse_lazy
from django.contrib.auth.forms import PasswordResetForm
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.conf import settings
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_encode
from django.utils.http import urlsafe_base64_decode
from .models import CustomUser
from django.utils.encoding import force_bytes


def page_view(request, page_name):
    titles = {
        "home": "Ivory Hospital - Home",
        "about": "Ivory Hospital - About Us",
        "contact": "Ivory Hospital - Contact Us",
        "services": "Ivory Hospital -  Our Services",
        "register": "Register",
        "login": "Login",
        "profile": "Your Profile",
        "menu": "Menu",
        "booking": "Booking",
    }
    title = titles.get(page_name, "Default Title")
    return render(request, f"{page_name}.html", {"page_title": title})


# Registration View
def register(request):
    if request.method == "POST":
        form = CustomUserCreationForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, "Registration successful. You can now log in.")
            return redirect("accounts:loginAccount")
        else:
            # Log detailed form errors
            print("Form errors:", form.errors.as_json())
            print("Form non-field errors:", form.non_field_errors())
    else:
        form = CustomUserCreationForm()
    return render(
        request, "accounts/register.html", {"form": form, "page_title": "Register"}
    )


# Login View
def loginUser(request):
    if request.method == "POST":
        form = CustomAuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect("accounts:profile")
        else:
            messages.error(request, "Invalid username or password.")
    else:
        form = CustomAuthenticationForm()
    return render(request, "accounts/login.html", {"form": form, "page_title": "Login"})


# Logout View
def logoutUser(request):
    logout(request)
    return redirect("accounts:loginAccount")


# Profile View
@login_required
def profile(request):
    if request.method == "POST":
        form = CustomUserChangeForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, "Profile updated successfully.")
            return redirect("accounts:profile")
    else:
        form = CustomUserChangeForm(instance=request.user)
    return render(
        request, "accounts/profile.html", {"form": form, "page_title": "Your Profile"}
    )


# Edit Profile View
@login_required
def edit_profile(request):
    if request.method == "POST":
        form = CustomUserChangeForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, "Profile updated successfully.")
            return redirect("accounts:profile")
    else:
        form = CustomUserChangeForm(instance=request.user)
    return render(
        request,
        "accounts/edit_profile.html",
        {"form": form, "page_title": "Edit Profile"},
    )


def password_reset_request(request):
    # Debugging statement to show the HTTP method used
    print(f"Request method: {request.method}")

    if request.method == "POST":
        form = PasswordResetForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data["email"]
            user = CustomUser.objects.filter(email=email).first()

            # Debugging statements
            print(f"Received POST request for password reset with email: {email}")
            if user:
                print(f"User found: {user.username}")
            else:
                print("No user found with the provided email.")

            if user:
                subject = "Password Reset Requested"
                email_template_name = "accounts/password_reset_email.html"
                context = {
                    "email": email,
                    "domain": request.META["HTTP_HOST"],
                    "site_name": "Ivory Hospital",
                    "protocol": "http",
                    "uid": urlsafe_base64_encode(force_bytes(user.pk)),
                    "token": default_token_generator.make_token(user),
                    "user": user,
                }

                # Debugging statement to check the context being sent in the email
                print("Context for password reset email:", context)

                email_body = render_to_string(email_template_name, context)
                plain_message = strip_tags(email_body)

                # Debugging statement to check the email content
                print("Email body content (HTML):", email_body)
                print("Email body content (Plain text):", plain_message)

                try:
                    send_mail(
                        subject,
                        plain_message,
                        settings.DEFAULT_FROM_EMAIL,
                        [email],
                        fail_silently=False,
                    )
                    print("Password reset email sent successfully.")
                except Exception as e:
                    print(f"Failed to send password reset email: {e}")

                messages.success(request, "Password reset email has been sent.")
                return redirect("accounts:password_reset_done")
            else:
                # You might want to handle the case where no user is found differently
                messages.error(request, "No account found with this email address.")
                return redirect("accounts:password_reset")
        else:
            # Log form errors for debugging
            print("Form errors:", form.errors.as_json())
            # If form is not valid, re-render the form with error messages
            print("Form non-field errors:", form.non_field_errors())
    else:
        form = PasswordResetForm()

    # Debugging statement to show the template rendering
    print("Rendering password_reset_form.html with form:", form)

    return render(
        request,
        "accounts/password_reset_form.html",
        {"form": form, "page_title": "Reset Password"},
    )


def password_reset_done(request):
    return render(
        request,
        "accounts/password_reset_done.html",
        {"page_title": "Password Reset Done"},
    )


def password_reset_confirm(request, uidb64, token):
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = CustomUser.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, CustomUser.DoesNotExist):
        user = None

    if user is not None and default_token_generator.check_token(user, token):
        if request.method == "POST":
            form = CustomSetPasswordForm(user, request.POST)
            if form.is_valid():
                form.save()
                messages.success(request, "Password has been reset successfully.")
                return redirect("accounts:password_reset_complete")
        else:
            form = CustomSetPasswordForm(user)
        return render(
            request,
            "accounts/password_reset_confirm.html",
            {"form": form, "page_title": "Reset Your Password"},
        )
    else:
        messages.error(request, "The password reset link is invalid or has expired.")
        return redirect("accounts:password_reset")


def password_reset_complete(request):
    return render(
        request,
        "accounts/password_reset_complete.html",
        {"page_title": "Password Reset Complete"},
    )
