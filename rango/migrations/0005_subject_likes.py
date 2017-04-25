# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('rango', '0004_auto_20170407_1159'),
    ]

    operations = [
        migrations.AddField(
            model_name='subject',
            name='likes',
            field=models.IntegerField(default=0),
            preserve_default=True,
        ),
    ]
