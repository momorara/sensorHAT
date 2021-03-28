#!/usr/bin/python
"""
###########################################################################
#Filename      :Lib_etc.py
#Author        :kawabata

いろんな関数をまとめてLib化します。
from nobu_LIB import Lib_etc

#Update        :2019/11/05
 　 　　　        2019/  
############################################################################
#
"""
import subprocess
import RPi.GPIO as GPIO
import time

#　ＣＰＵの温度を取得する。
def GetCpuTemp():
    Cmd = 'vcgencmd measure_temp'
    result = subprocess.Popen(Cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True)
    Rstdout ,Rstderr = result.communicate()
    CpuTemp = Rstdout.split()
    return CpuTemp[0]

#　ＬＥＤ#27 を点滅させる。
#  on 点灯時間　off 消灯時間　n 点滅回数
LEDPin27 = 27
def LED_flash27(on,off,n):
    for i in range(n):
        GPIO.output(LEDPin27,GPIO.HIGH)
        time.sleep(on)
        GPIO.output(LEDPin27,GPIO.LOW)
        time.sleep(off)


#　ＬＥＤ#22 を点滅させる。
#  on 点灯時間　off 消灯時間　n 点滅回数
LEDPin = 22
def LED_flash22(on,off,n):
    for i in range(n):
        GPIO.output(LEDPin,GPIO.LOW)
        time.sleep(on)
        GPIO.output(LEDPin,GPIO.HIGH)
        time.sleep(off)

#　ＳＷを読み取り、on off を返す。
def ReadSW(SW_PIN):
    if (GPIO.input(SW_Pin)):
        sw_ = 'off'
    else:
        sw_ = 'on'
    return sw_

def speakPrint(say_word):
    print(say_word)
    subprocess.run('~/julius/jsay_mei.sh ' + say_word,shell=True)
    return