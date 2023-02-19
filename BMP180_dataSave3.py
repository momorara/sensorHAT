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
2022/12/04  補正値の整備
2023/02/19  精度追求


scp -r sensorHAT pi@192.168.68.108:/home/pi
scp -r sensorHAT/*.py pi@192.168.68.126:/home/pi/sensorHAT
"""

# 補正値
hosei = 0


import datetime
import time
import Adafruit_BMP.BMP085 as BMP085
# import nobu_LIB.BMP085 as BMP085

# sensor = BMP085.BMP085()

try:
    sensor = BMP085.BMP085()
    press = ((sensor.read_pressure()+ 50)/ 100 )
except:
    try:
        time.sleep(1)
        sensor = BMP085.BMP085()
        press = ((sensor.read_pressure()+ 50)/ 100 )
    except:
        try:
            time.sleep(1.5)
            sensor = BMP085.BMP085()
            press = ((sensor.read_pressure()+ 50)/ 100 )
        except:
            time.sleep(3)
            sensor = BMP085.BMP085()
            press = ((sensor.read_pressure()+ 50)/ 100 )


print('測定値',end='', flush=True)
print('Pressure = ',press,'hPa' )

print('補正値　',end='', flush=True)
print(hosei)

print('補正後',end='', flush=True)
press = press + hosei
print('Pressure = ',press,'hPa' )

print('補正後int ',end='', flush=True)
press = int(press + 0.5)
print('Pressure = ',press,'hPa' )


time.sleep(0.5)
path = '/home/pi/sensorHAT/'
dt_now = datetime.datetime.now()
################## press ###################
# # 最新のデータを一つだけ入れたファイルを作る
press_s = str(dt_now) + "  :" + str(press) + '\n' 
# press_s = str(press)
with open(path + 'press_data.txt', mode='a') as f:
    f.write(press_s)
with open(path + 'press_data_last.txt', mode='w') as f:
    f.write(str(press))
############################################

