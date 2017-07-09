from django.db import models
from django.core.validators import RegexValidator
import datetime

class Token(models.Model):
    access_token = models.CharField(max_length = 200, blank = False)
    refresh_token = models.CharField(max_length = 200, blank = False)
    expires_timestamp = models.DateTimeField(blank = False)



class Appointment(models.Model):
    status_choices = (
        ('AR', 'Arrived'),
        ('NA', 'Not Arrived'),
        ('COM', 'Complete'),
        ('INS', 'In Session'),
    )
    id = models.AutoField(primary_key=True)
    pid = models.IntegerField(blank = False)   #used while updating demographic info
    first_name = models.CharField(max_length = 100, blank = False)
    last_name = models.CharField(max_length = 100, blank = False)
    SSN = models.CharField(max_length = 9, help_text = '*Please enter your 9 digit SSN without the dashes(-)', validators = [RegexValidator(regex='^[0-9]{9}$', message='SSN should be a 9 digit number', code='nomatch')], blank = False)
    time = models.DateTimeField(blank = False)
    check_in_time = models.DateTimeField(blank = False)
    duration = models.IntegerField(default = 15)
    wait_time = models.CharField(max_length = 10)
    status = models.CharField(max_length = 3, choices = status_choices, default = 'NA')
    checked_in = models.BooleanField(default = False)

#TODO:
#1) Add validators to model fields
#2) Figure out error_messages
