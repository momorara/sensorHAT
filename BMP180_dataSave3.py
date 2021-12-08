# –– coding: utf-8 –
#!/usr/bin/python
"""
BMPセンサーから気圧情報をとりだし、ファイル保存する

press_data.txt
BMP180_dataSave.py  python2で実行のこと
BMP180_dataSave3.py  python3で実行のこと

by.kawabata
2021/03/07  作成
2021/03/11  調整  
2021/03/13  温度データをファィルに書き込む 使用しないので、コメントとする

scp -r sensorHAT pi@192.168.68.126:/home/pi
scp -r sensorHAT pi@192.168.68.108:/home/pi
scp -r sensorHAT/*.py pi@192.168.68.126:/home/pi/sensorHAT
"""

import datetime
import time
import Adafruit_BMP.BMP085 as BMP085
# import nobu_LIB.BMP085 as BMP085
sensor = BMP085.BMP085()

# Temp Press
# print('Temp = {0:0.2f} *C'.format(sensor.read_temperature()))
# print('Pressure = {0:0.2f} Pa'.format(sensor.read_pressure()))
# print('Altitude = {0:0.2f} m'.format(sensor.read_altitude()))
# print('Sealevel Pressure = {0:0.2f} Pa'.format(sensor.read_sealevel_pressure()))
# print 'Pressure = ',sensor.read_pressure(),'hPa' 
print ('Temp = ',sensor.read_temperature())
dt_now = datetime.datetime.now()

temp = sensor.read_temperature()
# 気圧は、小数点第一位で四捨五入して、整数値にします。
# 信頼できる気圧値と違う場合は、補正する。直線性はあると仮定します。
hosei = 0
press = int((sensor.read_pressure()+ 50)/ 100 + hosei)
print('Pressure = ',press,'hPa' )

time.sleep(2.0)
path = '/home/pi/sensorHAT/'
################## press ###################
# # 最新のデータを一つだけ入れたファイルを作る
press_s = str(dt_now) + "  :" + str(press) + '\n' 
# press_s = str(press)
with open(path + 'press_data.txt', mode='a') as f:
    f.write(press_s)
with open(path + 'press_data_last.txt', mode='w') as f:
    f.write(str(press))
#####################################

# 本来ならDHT11の温度データを使用する設定だが、
# DHT11が不調の時やzeroでは取得できない場合があり、
# その時のバックアップとして、BMP180の温度をファイルに書き込む
# DHT11が正常な場合は、DHT11により上書きされたデータが使用される。
################## press ###################
# # 最新のデータを一つだけ入れたファイルを作る
# temp_s = str(dt_now) + "  :" + str(temp) + '\n' 
# with open(path + 'temp_data.txt', mode='a') as f:
#     f.write(temp_s)
# with open(path + 'temp_data_last.txt', mode='w') as f:
#     temp = int(temp * 10)
#     temp_s = str(temp)
#     f.write(temp_s)
#####################################