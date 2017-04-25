# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import DjangoUeditor.models


class Migration(migrations.Migration):

    dependencies = [
        ('rango', '0012_answers_categoryuserlikes'),
    ]

    operations = [
        migrations.CreateModel(
            name='BaiduEditor',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('content', DjangoUeditor.models.UEditorField(verbose_name='', blank=True)),
            ],
        ),
    ]
