# -*- coding: utf-8 -*-
# Generated by Django 1.9.5 on 2016-05-01 05:04
from __future__ import unicode_literals

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('moview', '0002_auto_20160501_0458'),
    ]

    operations = [
        migrations.AlterField(
            model_name='movie',
            name='release_date',
            field=models.DateField(verbose_name=datetime.datetime(2016, 5, 1, 5, 4, 27, 422287)),
        ),
        migrations.AlterField(
            model_name='movie',
            name='title',
            field=models.CharField(max_length=200, unique=True),
        ),
    ]
