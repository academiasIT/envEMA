# -*- coding: utf-8 -*-
# Generated by Django 1.11.6 on 2017-10-20 17:11
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('appEMA', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='estadoSensores',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('estadoSensorHumedad', models.BooleanField()),
                ('estadoSensorHuemdadSuelo', models.BooleanField()),
                ('estadoSensorLuz', models.BooleanField()),
                ('estadoSensorPresion', models.BooleanField()),
                ('estadoSensorTemperatura', models.BooleanField()),
                ('estadoSensorViento', models.BooleanField()),
            ],
        ),
    ]