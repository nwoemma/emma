from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser
from .forms import CustomUserCreationForm, CustomUserChangeForm


class CustomUserAdmin(UserAdmin):
    model = CustomUser
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm

    fieldsets = UserAdmin.fieldsets + (
        (
            None,
            {
                "fields": (
                    "role",
                    "department",
                    "specialty",
                    "date_of_birth",
                    "phone_number",
                )
            },
        ),
    )
    add_fieldsets = UserAdmin.add_fieldsets + (
        (
            None,
            {
                "fields": (
                    "role",
                    "department",
                    "specialty",
                    "date_of_birth",
                    "phone_number",
                )
            },
        ),
    )
    list_display = ["username", "email", "role", "phone_number"]
    search_fields = ("username", "email")
    ordering = ("username",)


admin.site.register(CustomUser, CustomUserAdmin)
