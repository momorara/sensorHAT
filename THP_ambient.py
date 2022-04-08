# -*- coding: utf-8 -*-
#!/usr/bin/python3

# AHT10とBMP180を連続して読み取り
# 温度T、湿度H、気圧PのCSVファィルを作ります。

# ambientにデータを投げます。

"""
Ambientライブラリのインストール
$ pip3 install git+https://github.com/AmbientDataInc/ambient-python-lib.git


2022/04/01  測定コアを作成
    01      とりあえずのエラー処理を組み込む
2022/04/02  1分に1回測定
    02      sensorHATのたの動作を邪魔しないように
            毎分10秒を過ぎた頃に計測します。
2022/04/03  リトライ
    03      異常データ
            AHT10 測定失敗時999とする
            BMP180  測定失敗時666
2022/04/06  
    01      THP_ambient.py

"""
import os
import time
import datetime
import smbus
import datetime
import time
import Adafruit_BMP.BMP085 as BMP085
import configparser

sensor = BMP085.BMP085()

path = '/home/pi/sensorHAT/'

# config,iniから値取得
# --------------------------------------------------
# configparserの宣言とiniファイルの読み込み
config_ini = configparser.ConfigParser()
config_ini.read(path + 'config.ini', encoding='utf-8')
# --------------------------------------------------
ch        =  int(config_ini.get('AMBIENT', 'ch'))
write_key =      config_ini.get('AMBIENT', 'write_key')
# --------------------------------------------------

# =================================================
#           ライブラリインポート
import ambient
import requests

# Ambient対応 
"""                チャネルID       ライトキー        """
# am = ambient.Ambient(49384, "bd093681d1a5a2c8")
am = ambient.Ambient(ch, write_key)
""""""""""""""""""""""""""""""""""""""""""""""""""""""

def data_read_BMP():
    hosei = 0
    try:
        press = int(((sensor.read_pressure()+ 50)/ 100 + hosei)*10)/10
    except:
        time.sleep(0.2)
        try:
            press = int(((sensor.read_pressure()+ 50)/ 100 + hosei)*10)/10
        except:
            press = 666
            # print('BMP180 error',datetime.datetime.now().second)
    return press


def data_read_AHT():
    try:
        # Get I2C bus
        #bus = smbus.SMBus(0)  # Rev 1 Pi uses 0
        bus = smbus.SMBus(1) # Rev 2 Pi uses 1
        # when you have a 121 IO Error, uncomment the next pause
        # time.sleep(1) #wait here to avoid 121 IO Error
        time.sleep(0.5)
        config = [0x08, 0x00]
        bus.write_i2c_block_data(0x38, 0xE1, config)
        time.sleep(0.5)
        # byt = bus.read_byte(0x38)
        #print(byt&0x68)
        MeasureCmd = [0x33, 0x00]
        bus.write_i2c_block_data(0x38, 0xAC, MeasureCmd)
        time.sleep(0.5)
        data = bus.read_i2c_block_data(0x38,0x00)
        temp = ((data[3] & 0x0F) << 16) | (data[4] << 8) | data[5]
        temp = ((temp*200) / 1048576) - 50
        temp = int(temp*10)/10
        # print(temp)
        humdy = ((data[1] << 16) | (data[2] << 8) | data[3]) >> 4
        humdy = int(humdy * 100 / 1048576)
        # print(humdy)
        hosei_temp  = 0
        hosei_humdy = 0
        temp  = temp  + hosei_temp
        humdy = humdy + hosei_humdy
    except:
        temp,humdy = 999,999
        # print('AHT10 error',datetime.datetime.now().second)
    return temp,humdy

def ambient(csv_data):
    print('ambient')
    try:
        res = am.send({"d1": csv_data[1],"d2": csv_data[2],"d3": csv_data[3]})
    except requests.exceptions.RequestException as e:
        print('request failed: ', e)

def main():
    print('start')

    header = ['time_stamp','temp','humdy','press']

    while True:

        if datetime.datetime.now().second > 10: # 10秒を超えたら計測

            # -------------------- BMP180 ----------------------
            for i in range(10):
                press = data_read_BMP()
                if press == 666 or press > 1060 or press < 800: # errorは10回までリトライします
                    time.sleep(0.4 * i/3 + 0.5)
                    if i > 3 :
                        temp,humdy = data_read_AHT()
                else:
                    break # errorがなければ、次に進む
            # -------------------- BMP180 ----------------------

            # -------------------- AHT10 ----------------------
            for i in range(10):
                temp,humdy = data_read_AHT()
                if temp == 999: # errorは10回までリトライします
                    time.sleep(0.4 * i/3 + 0.5)
                else:
                    break # errorがなければ、次に進む
            # -------------------- AHT10 ----------------------


            # -------------------- error表示 ----------------------
            if press == 666 or press > 1060 or press < 800: # error
                print('**** BMP180 err ****')
            if temp == 999: # error
                print('**** AHT10  err ****')
            # -------------------- error表示 ----------------------

            time_stamp = datetime.datetime.now().strftime('%Y/%m/%dT%H:%M')
            print(time_stamp,' temp:',temp,' humdy:',humdy ,' press:',press)

            csv_data = ['time_stamp','temp','humdy','press']
            csv_data[0] = time_stamp
            csv_data[1] = temp
            csv_data[2] = humdy
            csv_data[3] = press

            ambient(csv_data)

            while datetime.datetime.now().second > 10: # 毎分1回の計測に制限
                time.sleep(1)

        time.sleep(1)

if __name__ == '__main__':
    try:
        main()
    #when 'Ctrl+C' is pressed,child program destroy() will be executed.
    except KeyboardInterrupt:
        print('キーボード押されました。')
    except ValueError as e:
        print('err')
