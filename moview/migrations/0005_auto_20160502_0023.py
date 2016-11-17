# -*- coding: utf-8 -*-
# Generated by Django 1.9.5 on 2016-05-02 00:23
from __future__ import unicode_literals

import datetime
import django.contrib.postgres.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('moview', '0004_auto_20160502_0011'),
    ]

    operations = [
        migrations.AddField(
            model_name='moviematrix',
            name='context_feature',
            field=django.contrib.postgres.fields.ArrayField(base_field=models.FloatField(default=0), default=[0], size=None),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='movie',
            name='release_date',
            field=models.DateField(verbose_name=datetime.datetime(2016, 5, 2, 0, 23, 32, 634084)),
        ),
    ]
