# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('rango', '0020_answeruserdislikes_answeruserlikes'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='userprofile',
            name='user',
        ),
        migrations.RemoveField(
            model_name='campus',
            name='views',
        ),
        migrations.RemoveField(
            model_name='category',
            name='views',
        ),
        migrations.RemoveField(
            model_name='subject',
            name='likes',
        ),
        migrations.RemoveField(
            model_name='subject',
            name='views',
        ),
        migrations.AlterField(
            model_name='campus',
            name='name_ch',
            field=models.CharField(max_length=100),
        ),
        migrations.DeleteModel(
            name='UserProfile',
        ),
    ]
