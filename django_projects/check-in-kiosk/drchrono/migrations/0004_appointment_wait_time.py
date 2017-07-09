# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('drchrono', '0003_auto_20170111_0658'),
    ]

    operations = [
        migrations.AddField(
            model_name='appointment',
            name='wait_time',
            field=models.CharField(default='0', max_length=10),
            preserve_default=False,
        ),
    ]
