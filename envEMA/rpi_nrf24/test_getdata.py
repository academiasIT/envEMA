import RPi.GPIO as GPIO
from lib_nrf24 import NRF24
import spidev
import time
import ctypes
from struct import *
import sqlite3

GPIO.setmode(GPIO.BCM)

addr = [[0xe8, 0xe8, 0xf0, 0xf0, 0xe1], [0xf0, 0xf0, 0xf0, 0xf0, 0xe1]]

radio = NRF24(GPIO, spidev. SpiDev())
radio.begin(0, 25)
radio.setPayloadSize(32)
radio.setChannel(0x76)
radio.setDataRate(NRF24.BR_1MBPS)
radio.setPALevel(NRF24.PA_MIN)

radio.setAutoAck(True)
radio.enableDynamicPayloads()
radio.enableAckPayload()

radio.openWritingPipe(addr[0])
radio.openReadingPipe(1, addr[1])
radio.printDetails()
radio.stopListening()

def promedio(numeros):
    return float(sum(numeros)) / max(len(numeros), 1)


#inicializacion del sensor
CMD_START = list('a')
CMD_ACTIV_RELE = 0x02
TIME_OUT = 3
LECTURAS = []

db = sqlite3.connect('../sitioEMA/db.sqlite3')
radio.write(CMD_START)
radio.startListening()
print("(INFO) Sensor inicializado")
try:
    while(1):
        #Acumulacion de lecturas en un vector.
        if LECTURAS.__len__() <= 59:
            time_ini = time.time()
            print("Recibiendo datos del sensor...")
            while(not radio.available()):
                if (time.time() - time_ini) > TIME_OUT:
                    print("(WARNING) tiempo de espera agotado!")
                    print("(INFO) intentando inicializacion de sensores")
                    radio.stopListening()
                    radio.write(CMD_START)
                    radio.startListening()
                    time_ini = time.time()
            recv_msg = []
            radio.read(recv_msg, 24)
            recvb = pack('=24B', *recv_msg)
            result = unpack('=LffffHH', recvb)  # ulong,float x4, uint x2
            print("momento de la captura: ", str(result[0]))
            print("material particulado pm2.5: ", str(result[1]))
            print("material particulado pm10", str(result[2]))
            print("temperatura C: ", str(result[3]))
            print("humedad %: ", str(result[4]))
            print("monoxido de carbono : ", str(result[5]))
            print("ozono : ", str(result[6]))
            LECTURAS.append(result)
            print("Total de lecturas: ",LECTURAS.__len__())
        #Calculo de promedio por cada variable e insercion a la BD.
        if LECTURAS.__len__() == 60:
            #base de datos
            lecturas_pm25 = promedio([item[1] for item in LECTURAS])
            lecturas_pm10 = promedio([item[2] for item in LECTURAS])
            lecturas_temperatura = promedio([item[3] for item in LECTURAS])
            lecturas_humedad = promedio([item[4] for item in LECTURAS])
            lecturas_co = promedio([item[5] for item in LECTURAS])
            lecturas_o3 = promedio([item[6] for item in LECTURAS])

            dbc = db.cursor()
            date_muestreo = time.strftime('%Y-%m-%d %H:%M:%S')
            dbc.execute('''INSERT INTO appEMA_registroejecucion (fechaRegistro,origenMuestreo,detalleMuestreo) VALUES(?,?,?)''', (date_muestreo, "sensorX_test","Lectura automatizada."))
            print("Se crea el registro de lectura con id: "+str(dbc.lastrowid))
            dbc.execute('''INSERT INTO appEMA_sensorpm25 (idMuestreo_id,pm25) VALUES(?,?)''', (dbc.lastrowid, lecturas_pm25))
            dbc.execute('''INSERT INTO appEMA_sensorpm10 (idMuestreo_id,pm10) VALUES(?,?)''', (dbc.lastrowid, lecturas_pm10))
            dbc.execute('''INSERT INTO appEMA_sensortemperatura (idMuestreo_id,temperatura) VALUES(?,?)''', (dbc.lastrowid, lecturas_temperatura))
            dbc.execute('''INSERT INTO appEMA_sensorhumedad (idMuestreo_id,humedad) VALUES(?,?)''', (dbc.lastrowid, lecturas_humedad))
            dbc.execute('''INSERT INTO appEMA_sensorco (idMuestreo_id,co) VALUES(?,?)''', (dbc.lastrowid, float(lecturas_co)))
            dbc.execute('''INSERT INTO appEMA_sensoro3 (idMuestreo_id,o3) VALUES(?,?)''', (dbc.lastrowid, float(lecturas_o3)))

            db.commit()
            LECTURAS = []

except KeyboardInterrupt:
    print("cerrando base de datos...")
    db.close()
    pass



