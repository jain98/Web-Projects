# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('drchrono', '0002_remove_appointment_wait_time'),
    ]

    operations = [
        migrations.AlterField(
            model_name='appointment',
            name='check_in_time',
            field=models.DateTimeField(),
        ),
    ]
