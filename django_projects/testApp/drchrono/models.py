from django.db import models

# Create your models here.
class Token(models.Model):
    access_token = models.CharField(max_length = 200)
    refresh_token = models.CharField(max_length = 200)
    expires_timestamp = models.DateTimeField()
