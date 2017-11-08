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

#inicializacion del sensor
CMD_START = list('a')
CMD_ACTIV_RELE = 0x02
TIME_OUT = 3

db = sqlite3.connect('../sitioEMA/db.sqlite3')
radio.write(CMD_START)
radio.startListening()
print("(INFO) Sensor inicializado")
try:
    while(1):
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

        #base de datos
        dbc = db.cursor()
        date_muestreo = time.strftime('%Y-%m-%d %H:%M:%S')
        dbc.execute('''INSERT INTO appEMA_registroejecucion (fechaRegistro,origenMuestreo,detalleMuestreo) VALUES(?,?,?)''', (date_muestreo, "sensorX_test","Lectura automatizada."))
        print("Se crea el registro de lectura con id: "+str(dbc.lastrowid))
        # dbc.execute('''SELECT id from appSensores_registroEjecucion where id=(select max(id) from appSensores_sensormuestreo)''')
        # idm=dbc.fetchone()
        # dbc.execute('''INSERT INTO appSensores_sensorpm25 (idMuestreo_id,pm25) VALUES(?,?)''', (idm[0], result[1]))
        # dbc.execute('''INSERT INTO appSensores_sensorpm10 (idMuestreo_id,pm10) VALUES(?,?)''', (idm[0], result[2]))
        # dbc.execute('''INSERT INTO appSensores_sensortemperatura (idMuestreo_id,temperatura) VALUES(?,?)''', (idm[0], result[3]))
        # dbc.execute('''INSERT INTO appSensores_sensorhumedad (idMuestreo_id,humedad) VALUES(?,?)''', (idm[0], result[4]))
        # dbc.execute('''INSERT INTO appSensores_sensorco (idMuestreo_id,co) VALUES(?,?)''', (idm[0], float(result[5])))
        # dbc.execute('''INSERT INTO appSensores_sensoro3 (idMuestreo_id,o3) VALUES(?,?)''', (idm[0], float(result[6])))

        dbc.execute('''INSERT INTO appEMA_sensorpm25 (idMuestreo_id,pm25) VALUES(?,?)''', (dbc.lastrowid, result[1]))
        dbc.execute('''INSERT INTO appEMA_sensorpm10 (idMuestreo_id,pm10) VALUES(?,?)''', (dbc.lastrowid, result[2]))
        dbc.execute('''INSERT INTO appEMA_sensortemperatura (idMuestreo_id,temperatura) VALUES(?,?)''', (dbc.lastrowid, result[3]))
        dbc.execute('''INSERT INTO appEMA_sensorhumedad (idMuestreo_id,humedad) VALUES(?,?)''', (dbc.lastrowid, result[4]))
        dbc.execute('''INSERT INTO appEMA_sensorco (idMuestreo_id,co) VALUES(?,?)''', (dbc.lastrowid, float(result[5])))
        dbc.execute('''INSERT INTO appEMA_sensoro3 (idMuestreo_id,o3) VALUES(?,?)''', (dbc.lastrowid, float(result[6])))

        db.commit()

except KeyboardInterrupt:
    print("cerrando base de datos...")
    db.close()
    pass
