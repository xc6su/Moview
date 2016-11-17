# -*- coding: utf-8 -*-
# Generated by Django 1.9.5 on 2016-05-01 04:48
from __future__ import unicode_literals

import datetime
from django.conf import settings
import django.contrib.postgres.fields
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Movie',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200)),
                ('genre', django.contrib.postgres.fields.ArrayField(base_field=models.CharField(max_length=200), size=None)),
                ('director', django.contrib.postgres.fields.ArrayField(base_field=models.CharField(max_length=200), size=None)),
                ('rating', models.FloatField()),
                ('year', models.IntegerField()),
                ('poster', models.CharField(default='', max_length=200)),
                ('release_date', models.DateField(verbose_name=datetime.datetime(2016, 5, 1, 4, 48, 53, 554099))),
                ('detail_poster', models.CharField(default='', max_length=200)),
                ('rate_cnt', models.IntegerField(default=0)),
                ('duration', models.IntegerField(default=0)),
            ],
        ),
        migrations.CreateModel(
            name='MovieMatrix',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('vector', django.contrib.postgres.fields.ArrayField(base_field=models.FloatField(), size=None)),
                ('movie', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='moview.Movie', unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='Rate',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('rating', models.FloatField()),
                ('movie', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='moview.Movie')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='UserMatrix',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('vector', django.contrib.postgres.fields.ArrayField(base_field=models.FloatField(), size=None)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, unique=True)),
            ],
        ),
        migrations.AlterUniqueTogether(
            name='rate',
            unique_together=set([('user', 'movie')]),
        ),
    ]
