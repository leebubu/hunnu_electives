# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('rango', '0017_campus_name_ch'),
    ]

    operations = [
        migrations.AddField(
            model_name='subject',
            name='title_ch',
            field=models.CharField(max_length=100, blank=True),
        ),
    ]
