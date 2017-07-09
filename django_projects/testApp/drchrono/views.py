from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.core.mail import send_mail
from .forms import EmailForm
from . import api_methods
from models import Token
import datetime, pytz

''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
'''      Authentication view that fetches the Token object       '''
''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
def auth(request):
    response = api_methods.get_token(request)
    response.raise_for_status()
    data = response.json()
    # Save these in your database associated with the user
    token = Token.objects.create(
        access_token = data['access_token'],
        refresh_token = data['refresh_token'],
        expires_timestamp = datetime.datetime.now(pytz.utc) + datetime.timedelta(seconds=data['expires_in'])
    )
    token.save()
    return redirect("/options")


''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
'''                         Options Page                         '''
''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
def options(request):
    return render(request, 'options.html')


''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
'''           List of Patients with birthdays today              '''
''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
def birthdays(request):
    token = Token.objects.get(pk = 1)
    patients = api_methods.get_patients(token)
    form = EmailForm()
    return render(request, 'patients.html', {'patients': patients, 'form': form})


''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
'''         View and method to send emails to patients           '''
''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
def send_message(request):
    # Create form instance and populate it with data from request
    form = EmailForm(request.POST)
    # Check if form is valid
    if form.is_valid():
        send_email(form.cleaned_data)
        return redirect('/birthdays')   #Use AJAX instead of doing this

def send_email(emailform):
    subject, body, recipients = emailform['emailSubject'], emailform['emailBody'], emailform['patientEmailAddress'].split(',')
    send_mail(subject, body, 'kshitijjain2012@gmail.com', recipients, fail_silently = False,)
