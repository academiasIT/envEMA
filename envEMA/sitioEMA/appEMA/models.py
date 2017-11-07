# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models


# Create your models here.
class registroEjecucion(models.Model):
    fechaRegistro = models.DateField()
    origenMuestreo = models.TextField(max_length=10)
    detalleMuestreo = models.TextField()

class estadoSensores(models.Model):
    estadoSensorHumedad = models.BooleanField()
    estadoSensorHuemdadSuelo = models.BooleanField()
    estadoSensorLuz = models.BooleanField()
    estadoSensorPresion = models.BooleanField()
    estadoSensorTemperatura = models.BooleanField()
    estadoSensorViento = models.BooleanField()

class sensorpm25(models.Model):
    pm25 = models.FloatField()
    idMuestreo = models.ForeignKey(registroEjecucion, on_delete=models.CASCADE)

class sensorpm10(models.Model):
    pm10 = models.FloatField()
    idMuestreo = models.ForeignKey(registroEjecucion, on_delete=models.CASCADE)

class sensorco(models.Model):
    co = models.FloatField()
    idMuestreo = models.ForeignKey(registroEjecucion, on_delete=models.CASCADE)

class sensoro3():
    o3 = models.FloatField()
    idMuestreo = models.ForeignKey(registroEjecucion, on_delete=models.CASCADE)

class sensorTemperatura(models.Model):
    temperatura = models.FloatField()
    idMuestreo = models.ForeignKey(registroEjecucion, on_delete=models.CASCADE)

class sensorHumedad(models.Model):
    humedad = models.FloatField(validators=[MinValueValidator(0.0), MaxValueValidator(100.0)])
    idMuestreo = models.ForeignKey(registroEjecucion, on_delete=models.CASCADE)

class sensorHumedadSuelo(models.Model):
    humedad = models.FloatField(validators=[MinValueValidator(0.0), MaxValueValidator(100.0)])
    idMuestreo = models.ForeignKey(registroEjecucion, on_delete=models.CASCADE)

class sensorPresion(models.Model):
    presion = models.FloatField()
    idMuestreo = models.ForeignKey(registroEjecucion, on_delete=models.CASCADE)

class sensorViento(models.Model):
    kmPorHora = models.FloatField()
    idMuestreo = models.ForeignKey(registroEjecucion, on_delete=models.CASCADE)

class sensorLuz(models.Model):
    lux = models.FloatField()
    idMuestreo = models.ForeignKey(registroEjecucion, on_delete=models.CASCADE)
