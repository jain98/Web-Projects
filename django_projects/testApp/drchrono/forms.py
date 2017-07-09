from django import forms

# forms go here
class EmailForm(forms.Form):
    patientEmailAddress = forms.CharField(
        label='Patient Email',
        widget=forms.TextInput(attrs={
            'required': 'true',
            'class': 'form-control',
            'id': 'patientEmailAddress'}))

    emailSubject = forms.CharField(
        label='Subject',
        max_length=100,
        widget=forms.TextInput(attrs={
            'required': 'true',
            'class': 'form-control',
            'id': 'emailSubject'}))

    emailBody = forms.CharField(
        label='Body',
        widget=forms.Textarea(attrs={
            'required': 'true',
            'class': 'form-control',
            'id': 'emailBody',
            'rows': '3'
            }))
