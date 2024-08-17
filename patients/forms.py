from django import forms
from django.utils import timezone
from .models import Appointment


class AppointmentForm(forms.ModelForm):
    class Meta:
        model = Appointment
        fields = [
            "date",
            "reason",
            "doctor",
        ]  # Exclude 'status' as it will be set automatically

    date = forms.DateTimeField(
        widget=forms.DateTimeInput(attrs={"type": "datetime-local"}),
        input_formats=["%Y-%m-%dT%H:%M"],
    )

    def clean_date(self):
        date = self.cleaned_data.get("date")
        if date and timezone.is_naive(date):
            date = timezone.make_aware(date)
        return date
