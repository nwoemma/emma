from django import forms
from .models import Contact


class ContactForm(forms.ModelForm):
    recipient_role = forms.ChoiceField(
        choices=[("doctor", "Doctor"), ("patient", "Patient")]
    )

    class Meta:
        model = Contact
        fields = ["recipient_role", "email", "message"]
        widgets = {
            "recipient_role": forms.Select(attrs={"class": "form-control"}),
            "email": forms.EmailInput(attrs={"class": "form-control"}),
            "message": forms.Textarea(attrs={"class": "form-control"}),
        }

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop("request", None)
        super().__init__(*args, **kwargs)

    def save(self, commit=True):
        contact = super().save(commit=False)
        contact.user = self.request.user
        if commit:
            contact.save()
        return contact
