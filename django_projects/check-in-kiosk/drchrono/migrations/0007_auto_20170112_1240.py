# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.core.validators


class Migration(migrations.Migration):

    dependencies = [
        ('drchrono', '0006_auto_20170112_1058'),
    ]

    operations = [
        migrations.AlterField(
            model_name='appointment',
            name='SSN',
            field=models.IntegerField(help_text=b'*Please enter your 9 digit SSN without the dashes(-)', validators=[django.core.validators.RegexValidator(regex=b'^[0-9]{9}$', message=b'SSN should be a 9 digit number', code=b'nomatch')]),
        ),
    ]
