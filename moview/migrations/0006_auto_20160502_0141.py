# -*- coding: utf-8 -*-
# Generated by Django 1.9.5 on 2016-05-02 01:41
from __future__ import unicode_literals

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('moview', '0005_auto_20160502_0023'),
    ]

    operations = [
        migrations.AlterField(
            model_name='movie',
            name='release_date',
            field=models.DateField(verbose_name=datetime.datetime(2016, 5, 2, 1, 41, 44, 729941)),
        ),
    ]
