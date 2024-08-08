from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import CustomUser
from django.contrib.auth.forms import PasswordResetForm, SetPasswordForm


class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = (
            "username",
            "email",
            "role",
            "department",
            "specialty",
            "date_of_birth",
            "phone_number",
            "profile_picture",
        )


class CustomUserChangeForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = (
            "username",
            "email",
            "role",
            "department",
            "specialty",
            "date_of_birth",
            "phone_number",
            "profile_picture",
        )


class CustomAuthenticationForm(AuthenticationForm):
    class Meta:
        model = CustomUser
        fields = ("username", "password")


class CustomPasswordResetForm(PasswordResetForm):
    email = forms.EmailField(
        label="Email",
        max_length=254,
        widget=forms.EmailInput(attrs={"placeholder": "Enter your email address"}),
    )

    def clean_email(self):
        email = self.cleaned_data.get("email")
        if not CustomUser.objects.filter(email=email).exists():
            raise forms.ValidationError(
                "No user is associated with this email address."
            )
        return email


class CustomSetPasswordForm(SetPasswordForm):
    new_password1 = forms.CharField(
        label="New Password",
        widget=forms.PasswordInput(attrs={"placeholder": "Enter new password"}),
        strip=False,
        help_text="Enter a new password. The password must be at least 8 characters long and should not be easily guessable.",
    )
    new_password2 = forms.CharField(
        label="Confirm New Password",
        widget=forms.PasswordInput(attrs={"placeholder": "Confirm new password"}),
        strip=False,
    )

    def clean_new_password2(self):
        new_password1 = self.cleaned_data.get("new_password1")
        new_password2 = self.cleaned_data.get("new_password2")
        if new_password1 and new_password2 and new_password1 != new_password2:
            raise forms.ValidationError("The two password fields must match.")
        return new_password2
