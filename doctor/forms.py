from django import forms
from .models import DoctorAppointment


class DoctorAppointmentForm(forms.ModelForm):
    class Meta:
        model = DoctorAppointment
        fields = [
            "patient",
            "date",
            "reason",
        ]  # No doctor field here to prevent patient from setting it

    def __init__(self, *args, **kwargs):
        super(DoctorAppointmentForm, self).__init__(*args, **kwargs)
        self.fields["date"].widget.attrs.update({"class": "form-control"})
        self.fields["reason"].widget.attrs.update({"class": "form-control"})
