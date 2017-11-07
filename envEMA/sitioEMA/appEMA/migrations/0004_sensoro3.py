# -*- coding: utf-8 -*-
# Generated by Django 1.11.6 on 2017-11-07 16:58
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('appEMA', '0003_sensorco_sensorpm10_sensorpm25'),
    ]

    operations = [
        migrations.CreateModel(
            name='sensorO3',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('o3', models.FloatField()),
                ('idMuestreo', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='appEMA.registroEjecucion')),
            ],
        ),
    ]