from django import forms
from django.utils import timezone
from .models import Appointment


class AppointmentForm(forms.ModelForm):
    class Meta:
        model = Appointment
        fields = ["date", "reason"]  # Exclude 'status' as it will be set automatically

    date = forms.DateTimeField(
        widget=forms.DateTimeInput(format="%Y-%m-%d %H:%M:%S"),
        input_formats=["%Y-%m-%d %H:%M:%S"],
    )

    def clean_date(self):
        date = self.cleaned_data.get("date")
        if date and timezone.is_naive(date):
            date = timezone.make_aware(date)
        return date
