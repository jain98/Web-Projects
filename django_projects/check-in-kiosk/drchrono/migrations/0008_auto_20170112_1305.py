# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.core.validators


class Migration(migrations.Migration):

    dependencies = [
        ('drchrono', '0007_auto_20170112_1240'),
    ]

    operations = [
        migrations.AlterField(
            model_name='appointment',
            name='SSN',
            field=models.CharField(help_text=b'*Please enter your 9 digit SSN without the dashes(-)', max_length=9, validators=[django.core.validators.RegexValidator(regex=b'^[0-9]{9}$', message=b'SSN should be a 9 digit number', code=b'nomatch')]),
        ),
    ]
