from django import forms
from .models import Booking


class TableForm(forms.ModelForm):
    Name = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Name'}))
    Phone = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Phone Number'}))
    email = forms.EmailField(widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Email'}))
    no_of_persons = forms.IntegerField(widget=forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'No of Persons'}))
    date = forms.DateField(
        widget=forms.DateInput(attrs={'class': 'form-control', 'placeholder': 'Date'}),
    )
    
    class Meta:
        model = Booking
        fields = ['Name', 'Phone', 'email', 'no_of_persons', 'date']


    def clean(self):
        cleaned_data = super().clean()
        name = cleaned_data.get('Name')
        phone = cleaned_data.get('Phone')
        email = cleaned_data.get("email")
        if not name or not phone or not email:
            raise forms.ValidationError("Email is not valid.")
    
        return cleaned_data

