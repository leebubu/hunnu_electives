# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('rango', '0008_auto_20170407_1355'),
    ]

    operations = [
        migrations.AddField(
            model_name='category',
            name='slug',
            field=models.SlugField(default=12, unique=True),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='subject',
            name='slug',
            field=models.SlugField(default=123, unique=True),
            preserve_default=False,
        ),
    ]
