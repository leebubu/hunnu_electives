# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('rango', '0013_baidueditor'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='subject',
            name='category',
        ),
        migrations.AddField(
            model_name='category',
            name='subject',
            field=models.ForeignKey(default=123, to='rango.Subject'),
            preserve_default=False,
        ),
    ]
