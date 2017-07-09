from django import forms
from django.core.validators import RegexValidator

class DemographicInfoForm(forms.Form):
    gender_choices = (('Male', 'Male'), ('Female', 'Female'), ('Other', 'Other'))
    ethnicity_choices = (('hispanic', 'Hispanic'), ('not_hispanic', 'Not Hispanic'), ('declined', 'Declined'))

    email = forms.CharField(
        label='Patient Email',
        widget=forms.EmailInput(attrs={
            'required': 'true',
            'class': 'form-control',
            'id': 'email'}))

    address = forms.CharField(
        label='Patient Address',
        widget=forms.TextInput(attrs={
            'required': 'true',
            'class': 'form-control',
            'id': 'address'}))


    cell_phone = forms.CharField(
        label='Patient Cell',
        widget=forms.TextInput(attrs={
            'required': 'true',
            'class': 'form-control',
            'id': 'cell_phone',
            'maxlength':'12'}),
        help_text = '*Please enter you contact number separated by dashes(-)',
        validators = [RegexValidator(regex='^[0-9]{3}-[0-9]{3}-[0-9]{4}$', message='Invalid phone number!', code='nomatch')]
        )

    gender = forms.ChoiceField(
        label='Patient Gender',
        choices = gender_choices)

    ethnicity = forms.ChoiceField(
        label='Patient Ethnicity',
        choices = ethnicity_choices)
