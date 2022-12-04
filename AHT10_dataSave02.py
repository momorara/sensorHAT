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
2021/04/25  board,busio,adafruit_ahtx0を使わない方法
    02
2022/03/06  AHT10がない場合に、BMPの温度を使用する。
2022/12/04  補正値の整備

scp -r sensorHAT pi@192.168.68.108:/home/pi
scp -r sensorHAT/*.py pi@192.168.68.126:/home/pi/sensorHAT
"""

# 補正値
temp_hosei  = 0
humdy_hosei = 0


import time
# import board
# import busio
# import adafruit_ahtx0
import datetime
import smbus
import Adafruit_BMP.BMP085 as BMP085

path = '/home/pi/sensorHAT/'


def data_read():
    # Get I2C bus
    #bus = smbus.SMBus(0)  # Rev 1 Pi uses 0
    bus = smbus.SMBus(1) # Rev 2 Pi uses 1
    # when you have a 121 IO Error, uncomment the next pause
    # time.sleep(1) #wait here to avoid 121 IO Error

    config = [0x08, 0x00]
    bus.write_i2c_block_data(0x38, 0xE1, config)
    time.sleep(0.5)
    byt = bus.read_byte(0x38)
    #print(byt&0x68)
    MeasureCmd = [0x33, 0x00]
    bus.write_i2c_block_data(0x38, 0xAC, MeasureCmd)
    time.sleep(0.5)

    data = bus.read_i2c_block_data(0x38,0x00)

    temp = ((data[3] & 0x0F) << 16) | (data[4] << 8) | data[5]
    temp = ((temp*200) / 1048576) - 50
    temp = int(temp*10)/10

    humdy = ((data[1] << 16) | (data[2] << 8) | data[3]) >> 4
    humdy = int(humdy * 100 / 1048576)
    return temp,humdy


# i2c接続がない場合のエラーでは何もせずに終了する。
try:
    # sensor = adafruit_ahtx0.AHTx0(i2c)

    # temp = sensor.temperature
    # humdy = sensor.relative_humidity

    try:
        temp,humdy = data_read()
    except:
        time.sleep(2)
        temp,humdy = data_read()


    print('測定値',end='', flush=True)
    print("Temperature: %0.1f C" % temp, end='', flush=True)
    print("   Humidity: %0.1f %%" % humdy)

    print('補正値        ',end='', flush=True)
    print('温度:',temp_hosei,'           湿度:',humdy_hosei)

    print('補正後',end='', flush=True)
    temp = temp + temp_hosei
    humdy = int(humdy + humdy_hosei)
    print("Temperature: %0.1f C" % temp, end='', flush=True)
    print("   Humidity: %0.1f %%" % humdy)


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
    ############################################
    ################## humdy ###################
    # # 最新のデータを一つだけ入れたファイルを作る
    humdy_s = dt_now.strftime("%Y/%m/%d %H:%M.%S") + "  :" + str(humdy) + '\n' 
    with open(path + 'humdy_data.txt', mode='a') as f:
        f.write(humdy_s)
    with open(path + 'humdy_data_last.txt', mode='w') as f:
        f.write(str(humdy))
    ############################################

# AHTがない場合に温度をBMPから取得する。
except:
    pass
    print('**** AHT error の場合のBMPの値****')
    try:
        sensor = BMP085.BMP085()
        temp = sensor.read_temperature()
        print("Temperature: %0.1f C" % temp, end='', flush=True)
        print("  Humidity:  no data")
        dt_now = datetime.datetime.now()
        temp_s = str(dt_now) + "  :" + str(temp) + '\n' 
        with open(path + 'temp_data.txt', mode='a') as f:
            f.write(temp_s)
        with open(path + 'temp_data_last.txt', mode='w') as f:
            temp = int(temp * 10)
            temp_s = str(temp)
            f.write(temp_s)
            
        # 湿度データを消す
        with open(path + 'humdy_data_last.txt', mode='w') as f:
            f.write('0')
    except:
        print('**** BMP error ****')