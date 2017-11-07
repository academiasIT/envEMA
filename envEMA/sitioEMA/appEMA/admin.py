# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin

# Register your models here.
from .models import registroEjecucion, \
    sensorTemperatura, \
    sensorHumedad, \
    sensorHumedadSuelo, \
    sensorPresion, \
    sensorViento, \
    sensorLuz, \
    estadoSensores, sensorCo, sensorPm25, sensorPm10, sensorO3

admin.site.register(registroEjecucion)
admin.site.register(sensorTemperatura)
admin.site.register(sensorHumedad)
admin.site.register(sensorHumedadSuelo)
admin.site.register(sensorPresion)
admin.site.register(sensorViento)
admin.site.register(sensorLuz)
admin.site.register(estadoSensores)
admin.site.register(sensorCo)
admin.site.register(sensorPm25)
admin.site.register(sensorPm10)
admin.site.register(sensorO3)
