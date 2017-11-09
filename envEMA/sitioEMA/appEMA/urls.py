from django.conf.urls import url

from . import views

from . import views
from jchart.views import ChartView
from views import graficaTemperatura, graficaHumedad

grafica_temp = graficaTemperatura()
grafica_hum = graficaHumedad()

urlpatterns = [
    #ejemplo: /home/
    url(r'^$', views.index, name='index'),
    url(r'^estadoSensores/$', views.estadoActualSensores, name='estadoSensores'),
    url(r'^estadoConexion/$', views.estadoConexion, name='estadoConexion'),
    url(r'^datosPublicos/$', views.datosPublicos, name='datosPublicos'),
    url(r'^graficos/$', views.graficos, name='graficos'),
    url(r'^ultimasMediciones/$', views.ultimasMediciones, name='ultimasMediciones'),
    url(r'^sensorHumedad/$', views.sensorHumedadDetalle, name='sensorHumedad'),
    url(r'^sensorHumedadSuelo/$', views.sensorHumedadSueloDetalle, name='sensorHumedadSuelo'),
    url(r'^sensorLuz/$', views.sensorLuzDetalle, name='sensorLuz'),
    url(r'^sensorPresionAtmosferica/$', views.sensorPresionAtmosfericaDetalle, name='sensorPresionAtmosferica'),
    url(r'^sensorTemperatura/$', views.sensorTemperaturaDetalle, name='sensorTemperatura'),
    url(r'^sensorViento/$', views.sensorVientoDetalle, name='sensorViento'),
    url(r'^charts/line_temperatura/$', ChartView.from_chart(grafica_temp), name='plot_temperaturas'),
    url(r'^charts/line_humedad/$', ChartView.from_chart(grafica_hum), name='plot_humedad'),
]