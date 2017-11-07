# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import urllib2

from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponse
from django.shortcuts import render
from django.template import loader

from .models import *


def index(request):
    template = loader.get_template('appEMA/index.html')
    return HttpResponse(template.render())

def graficos(request):
    template = loader.get_template('appEMA/graficos.html')
    return HttpResponse(template.render())
def datosPublicos(request):
    template = loader.get_template('appEMA/datosPublicos.html')
    return HttpResponse(template.render())

def estadoActualSensores(request):
    try:
        detalleEstadoSensores = estadoSensores.objects.get()
    except ObjectDoesNotExist:
        detalleEstadoSensores = None
    return render(request,'appEMA/estadoSensores.html', {
        'detalleEstadoSensores':detalleEstadoSensores
    })

def estadoConexion(request):
    #template = loader.get_template('appEMA/estadoConexion.html')
    #return HttpResponse(template.render())
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')

    try:
        urllib2.urlopen('http://google.cl', timeout=1)
        estadoConexionActual = True
    except urllib2.URLError as err:
        estadoConexionActual = False


    return render(request,'appEMA/estadoConexion.html',{'ipRecibida':ip, 'estadoConexion':estadoConexionActual})

def ultimasMediciones(request):
    try:
        ultimoRegistroSensores = registroEjecucion.objects.filter().order_by('-id')[0]
        try:
            detalleTemperatura = sensorTemperatura.objects.get(idMuestreo=ultimoRegistroSensores.id)
        except ObjectDoesNotExist:
            detalleTemperatura = None
        try:
            detalleHumedad = sensorHumedad.objects.get(idMuestreo=ultimoRegistroSensores.id)
        except ObjectDoesNotExist:
            detalleHumedad = None
        try:
            detalleHumedadPiso = sensorHumedadSuelo.objects.get(idMuestreo=ultimoRegistroSensores.id)
        except ObjectDoesNotExist:
            detalleHumedadPiso = None
        try:
            detalleLuz = sensorLuz.objects.get(idMuestreo=ultimoRegistroSensores.id)
        except ObjectDoesNotExist:
            detalleLuz = None
        try:
            detallePresion = sensorPresion.objects.get(idMuestreo=ultimoRegistroSensores.id)
        except ObjectDoesNotExist:
            detallePresion = None
        try:
            detalleViento = sensorViento.objects.get(idMuestreo=ultimoRegistroSensores.id)
        except ObjectDoesNotExist:
            detalleViento = None
        try:
            detallePm25 = sensorPm25.objects.get(idMuestreo=ultimoRegistroSensores.id)
        except ObjectDoesNotExist:
            detallePm25 = None
        try:
            detallePm10 = sensorPm10.objects.get(idMuestreo=ultimoRegistroSensores.id)
        except ObjectDoesNotExist:
            detallePm10 = None
        try:
            detalleCo = sensorCo.objects.get(idMuestreo=ultimoRegistroSensores.id)
        except ObjectDoesNotExist:
            detalleCo = None
        try:
            detalleO3=sensorO3.objects.get(idMuestreo=ultimoRegistroSensores.id)
        except ObjectDoesNotExist:
            detalleO3 = None

    except ObjectDoesNotExist:
        ultimoRegistroSensores = None

    return render(request,'appEMA/ultimasMediciones.html',{
        'ultimoRegistroSensores':ultimoRegistroSensores,
        'detalleHumedad':detalleHumedad,
        'detalleHumedadPiso':detalleHumedadPiso,
        'detalleTemperatura':detalleTemperatura,
        'detalleLuz':detalleLuz,
        'detallePresion':detallePresion,
        'detalleViento':detalleViento,
        'detallePm25':detallePm25,
        'detallePm10':detallePm10,
        'detalleCo':detalleCo,
        'detalleO3':detalleO3
    })

def sensorHumedadDetalle(request):
    template = loader.get_template('appEMA/sensorHumedad.html')
    return HttpResponse(template.render())


def sensorHumedadSueloDetalle(request):
    template = loader.get_template('appEMA/sensorHumedadSuelo.html')
    return HttpResponse(template.render())

def sensorLuzDetalle(request):
    template = loader.get_template('appEMA/sensorLuz.html')
    return HttpResponse(template.render())

def sensorPresionAtmosfericaDetalle(request):
    template = loader.get_template('appEMA/sensorPresionAtmosferica.html')
    return HttpResponse(template.render())

def sensorTemperaturaDetalle(request):
    template = loader.get_template('appEMA/sensorTemperatura.html')
    return HttpResponse(template.render())

def sensorVientoDetalle(request):
    template = loader.get_template('appEMA/sensorViento.html')
    return HttpResponse(template.render())
