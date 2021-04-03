# -*- coding: utf-8 -*-
#!/usr/bin/python3

# AHT10_02.py
"""
pip install adafruit-circuitpython-ahtx0
でインストールすると使えます。MITライセンスとのこと

2021/03/30  ライブラリを改造してsensorHATで使えるようにする
            zeroで使えないDHT11の代替え
            1度だけ測定して、ファイルに書き込む
2021/04/02  i2c接続がない場合のエラー処理を追加


scp -r sensorHAT/*.py pi@192.168.68.128:/home/pi/sensorHAT
scp -r sensorHAT pi@192.168.68.128:/home/pi
"""

import time
import board
import busio
import adafruit_ahtx0
import datetime

path = '/home/pi/sensorHAT/'

# Create library object using our Bus I2C port
i2c = busio.I2C(board.SCL, board.SDA)
# print(i2c)

# i2c接続がない場合のエラーでは何もせずに終了する。
try:
    sensor = adafruit_ahtx0.AHTx0(i2c)

    temp = sensor.temperature
    humdy = sensor.relative_humidity

    print("Temperature: %0.1f C" % temp, end='', flush=True)
    print("  Humidity: %0.1f %%" % humdy)
    # time.sleep(5)

    temp = temp
    humdy = str(int(humdy))

    dt_now = datetime.datetime.now()
    s = "摂氏: {0:.1f}"
    ################## temp ###################
    # # 最新のデータを一つだけ入れたファイルを作る
    temp_s = dt_now.strftime("%Y/%m/%d %H:%M.%S") + " :" + s.format(temp) + '\n' 
    with open(path + 'temp_data.txt', mode='a') as f:
        f.write(temp_s)
    with open(path + 'temp_data_last.txt', mode='w') as f:
        s = "{0:.1f}"
        temp = int(temp * 10)
        temp_s = str(temp)
        f.write(temp_s)
    #####################################
    ################## humdy ###################
    # # 最新のデータを一つだけ入れたファイルを作る
    humdy_s = dt_now.strftime("%Y/%m/%d %H:%M") + "  :" + humdy + '\n' 
    with open(path + 'humdy_data.txt', mode='a') as f:
        f.write(humdy_s)
    with open(path + 'humdy_data_last.txt', mode='w') as f:
        f.write(humdy)
    #####################################

except:
    pass
    # print('**** i2c error ****')