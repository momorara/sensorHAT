#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
SR04_dataSave.py

HY-SRF05超音波距離センサモジュールを使い、距離を測定しファイルに保存します。

0.05秒毎に4回計測して、最後の値をとる。計測は1回のみ
(平均を取ったり、最大最少をのぞいて平均したり色々考えられる)

書き出しファイル
    dist_data.txt
    dist_data_last.txt

by.kawabata

2021/03/07  作成


scp -r sensorHAT/*.py pi@192.168.68.126:/home/pi/sensorHAT
scp -r sensorHAT pi@192.168.68.126:/home/pi
'''
import datetime
import RPi.GPIO as GPIO
import time

# TRIGとECHOのGPIO番号   
TRIG_PIN = 24
ECHO_PIN = 23
# ピン番号をGPIOで指定
GPIO.setmode(GPIO.BCM)
# TRIG_PINを出力, ECHO_PINを入力
GPIO.setup(TRIG_PIN,GPIO.OUT)
GPIO.setup(ECHO_PIN,GPIO.IN)
GPIO.setwarnings(False)


# HIGH or LOWの時計測
def pulseIn(PIN, start=1, end=0):
    if start==0: end = 1
    t_start = 0
    t_end = 0
    # ECHO_PINがHIGHである時間を計測
    while GPIO.input(PIN) == end:
        t_start = time.time()
        
    while GPIO.input(PIN) == start:
        t_end = time.time()
    return t_end - t_start

# 距離計測
def calc_distance(TRIG_PIN, ECHO_PIN, num, v=34000): 
    for i in range(num):
        # TRIGピンを0.3[s]だけLOW
        GPIO.output(TRIG_PIN, GPIO.LOW)
        time.sleep(0.3)
        # TRIGピンを0.00001[s]だけ出力(超音波発射)        
        GPIO.output(TRIG_PIN, True)
        time.sleep(0.00001)
        GPIO.output(TRIG_PIN, False)
        # HIGHの時間計測
        t = pulseIn(ECHO_PIN)
        # 距離[cm] = 音速[cm/s] * 時間[s]/2
        distance = v * t/2
        # print(distance, "cm")
        time.sleep(0.05)
    # ピン設定解除
    GPIO.cleanup()
    return int(distance*10)/10

path = '/home/pi/sensorHAT/'
def main():
    # 距離計測(TRIGピン番号, ECHO_PIN番号, 計測回数, 音速[cm/s])
    dist = calc_distance(TRIG_PIN, ECHO_PIN, 3, 34000)
    print(dist)
    #
    # 0.05秒毎に4回計測して、最後の値をとる
    # 
    dt_now = datetime.datetime.now()
    # dist = 単位は cm 
    ################## dist ###################
    # # 最新のデータを一つだけ入れたファイルを作る
    dist_s = dt_now.strftime("%Y/%m/%d %H:%M") + "  :" + str(dist) + ' cm \n' 
    # print(dist_s)
    with open(path + 'dist_data.txt', mode='a') as f:
        f.write(dist_s)
    with open(path + 'dist_data_last.txt', mode='w') as f:
        f.write(str(dist))
    #####################################

    


if __name__ == '__main__':
    try:
        main()

    except KeyboardInterrupt:
        print("key入力がありましたので、プログラム停止" )
    except ValueError as e:
        print(e)
