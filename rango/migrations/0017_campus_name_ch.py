# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('rango', '0016_campus_views'),
    ]

    operations = [
        migrations.AddField(
            model_name='campus',
            name='name_ch',
            field=models.CharField(max_length=100, blank=True),
        ),
    ]
