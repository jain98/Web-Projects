# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('drchrono', '0004_appointment_wait_time'),
    ]

    operations = [
        migrations.AddField(
            model_name='appointment',
            name='checked_in',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='appointment',
            name='SSN',
            field=models.CharField(max_length=9),
        ),
        migrations.AlterField(
            model_name='appointment',
            name='pid',
            field=models.IntegerField(),
        ),
    ]
