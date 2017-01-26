# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-01-07 09:35
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0006_auto_20161223_0958'),
    ]

    operations = [
        migrations.AlterField(
            model_name='news',
            name='header',
            field=models.CharField(blank=True, max_length=255, verbose_name='Title'),
        ),
        migrations.AlterField(
            model_name='news',
            name='site',
            field=models.CharField(choices=[('HABRAHABR', 'HABRAHABR'), ('GEEKTIMES', 'GEEKTIMES'), ('TPROGER', 'TPROGER'), ('GAGADGET', 'GAGADGET'), ('AIN', 'AIN'), ('ITMENTOR', 'ITMENTOR')], max_length=255),
        ),
    ]
