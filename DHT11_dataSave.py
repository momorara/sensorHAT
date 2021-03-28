#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
test_DHT11.py
温湿度センサモジュール(DHT11) を使い、温度・湿度を測定します。
ダウンロードしたDHT11のプログラムを使う

DHT11_dataSave.py

起動後2.5秒ごに測定し、データがあれば
測定した温度、湿度をファイルに保存します。
データが取得できてなかったら2.5秒後に再度測定する。
これを20回繰り返し、データが取得できなかったらプログラム終了する。
temp_data.txt中の最後の数字がリトライ回数-1です。そこそこリトライしていますね。
書き出しファイル
    temp_data.txt
    humdy_dqtq.txt
    +_last

by.kawabata
2021/03/07  作成
2021/03/11  20回リトライするとzeroだと1分を超えてしまうので、15回とした。
2021/03/28  2B,3Bでは問題なくデータを取得できるが、zeroでは取得できない。
            プルアップを変えても、#14でもダメだった。


scp -r sensorHAT/*.py pi@192.168.68.128:/home/pi/sensorHAT
scp -r sensorHAT pi@192.168.68.128:/home/pi

'''

import RPi.GPIO as GPIO
import time
import datetime
from nobu_LIB import Lib_dht11
# import dht11

path = '/home/pi/sensorHAT/'

# initialize GPIO
GPIO.setwarnings(True)
GPIO.setmode(GPIO.BCM)

# read data using pin 25
instance = Lib_dht11.DHT11(pin=25)

n_kai = 0
temp_s = ''
humdy_s = ''
temp  = -1
humdy = -1
try:
    while temp == -1 and humdy == -1:
        time.sleep(2.5)
        
        temp  = -1
        humdy = -1
        n_kai += 1

        result = instance.read()
        if result.is_valid():

            # print("Last valid input: " + str(datetime.datetime.now()))
            # print("温度: %-3.1f C" % result.temperature)
            # print("湿度: %-3.1f %%" % result.humidity)
            
            temp = result.temperature
            humdy = str(int(result.humidity))
                
            # s = "摂氏: {0:.1f}"
            # print(dt_now.strftime("%Y/%m/%d %H:%M")," :",s.format(temp),'度/',humdy,'%')
        
        # 
        print(n_kai,temp,humdy)

        #20回を超えたらプログラム終了 データ欠損
        if n_kai > 15:
            dt_now = datetime.datetime.now()
            s = "摂氏: {0:.1f}"
            ################## temp ###################
            # # 最新のデータを一つだけ入れたファイルを作る
            temp_s = dt_now.strftime("%Y/%m/%d %H:%M.%S") + " :" + 'データ欠損' + ' /' + str(n_kai) + '\n' 
            with open(path + 'temp_data.txt', mode='a') as f:
                f.write(temp_s)
            #####################################
            print("Cleanup")
            GPIO.cleanup()
            exit(0)

    dt_now = datetime.datetime.now()
    s = "摂氏: {0:.1f}"
    ################## temp ###################
    # # 最新のデータを一つだけ入れたファイルを作る
    temp_s = dt_now.strftime("%Y/%m/%d %H:%M.%S") + " :" + s.format(temp) + ' /' + str(n_kai) + '\n' 
    # temp_s = dt_now.strftime("%Y/%m/%d %H:%M.%S") + " :" + s.format(temp) + '\n' 
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
    
    print("Cleanup")
    GPIO.cleanup()

except KeyboardInterrupt:
    print("Cleanup")
    GPIO.cleanup()