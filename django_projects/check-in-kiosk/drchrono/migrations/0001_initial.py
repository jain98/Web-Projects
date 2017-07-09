# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Appointment',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True)),
                ('pid', models.CharField(max_length=8)),
                ('first_name', models.CharField(max_length=100)),
                ('last_name', models.CharField(max_length=100)),
                ('SSN', models.CharField(max_length=12)),
                ('time', models.DateTimeField()),
                ('check_in_time', models.DateTimeField(null=True)),
                ('wait_time', models.FloatField(null=True)),
                ('duration', models.IntegerField(default=15)),
                ('status', models.CharField(default=b'NA', max_length=3, choices=[(b'AR', b'Arrived'), (b'NA', b'Not Arrived'), (b'COM', b'Complete'), (b'INS', b'In Session')])),
            ],
        ),
        migrations.CreateModel(
            name='Token',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('access_token', models.CharField(max_length=200)),
                ('refresh_token', models.CharField(max_length=200)),
                ('expires_timestamp', models.DateTimeField()),
            ],
        ),
    ]
