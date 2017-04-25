# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('rango', '0015_auto_20170411_2105'),
    ]

    operations = [
        migrations.AddField(
            model_name='campus',
            name='views',
            field=models.IntegerField(default=0),
        ),
    ]
