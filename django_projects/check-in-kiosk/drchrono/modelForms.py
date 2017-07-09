from django import forms
from models import *


class AppointmentForm(forms.ModelForm):
    class Meta:
        model = Appointment
        fields = ['first_name', 'last_name', 'SSN']
        widgets = {
        'first_name': forms.TextInput(attrs={'required': 'true', 'class': 'form-control', 'id': 'first_name'}),
        'last_name' : forms.TextInput(attrs={'required': 'true', 'class': 'form-control', 'id': 'last_name'}),
        'SSN' : forms.TextInput(attrs={'required': 'true', 'maxlength': '9', 'class': 'form-control', 'id': 'ssn'})
        }
