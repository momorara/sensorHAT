#!/usr/bin/python
"""
###########################################################################
#Filename      :test_ADC.py
#Author        :kawabata

MCP3002用に改変した。

ADCを2chで駆動する。

起動して一度だけch0のデータを取得する

#Update        :2019/10/17
#Update        :2019/10/26
#Update        :2019/11/02
2021/12/03  MCP3002用に修正
2021/12/07  一度だけデータ取得しておわり　node-red用

############################################################################
scp -r sensorHAT/MCP*.py pi@172.20.10.6:/home/pi/sensorHAT
"""
# from nobu_LIB import Lib_ADC
import time
import os
import RPi.GPIO as GPIO
import random

SPICLK = 11
SPIMISO = 9
SPIMOSI = 10
SPICS = 8

#print message at the begining ---custom function
def print_message():
    print ('Program is running...')
    print ('Please press Ctrl+C to end the program...')

def setup():
    GPIO.setwarnings(False)
    #set the gpio modes to BCM numbering
    GPIO.setmode(GPIO.BCM)
    # set up the SPI interface pins
    GPIO.setup(SPIMOSI, GPIO.OUT)
    GPIO.setup(SPIMISO, GPIO.IN)
    GPIO.setup(SPICLK, GPIO.OUT)
    GPIO.setup(SPICS, GPIO.OUT)
    # safePowerのRy_offをプルダウンにする
    GPIO.setup(20, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

def readadc(adcnum):
    if adcnum == 0: adcnum=2
    if adcnum > 2 or adcnum < 0: return -1
    GPIO.output(SPICS, True)
    GPIO.output(SPICLK, False)  # start clock low
    GPIO.output(SPICS, False)   # bring CS low

    commandout = adcnum
    commandout |= 0x0d  # start bit + single-ended bit
    commandout <<= 3    # we only need to send 5 bits here
    for i in range(4):
        if commandout & 0x80:
            GPIO.output(SPIMOSI, True)
        else:
            GPIO.output(SPIMOSI, False)
        commandout <<= 1
        GPIO.output(SPICLK, True)
        GPIO.output(SPICLK, False)

    adcout = 0
    # read in one empty bit, one null bit and 10 ADC bits
    for i in range(12):
        GPIO.output(SPICLK, True)
        GPIO.output(SPICLK, False)
        adcout <<= 1
        if (GPIO.input(SPIMISO)):
            adcout |= 0x1
    GPIO.output(SPICS, True)
    adcout >>= 1       # first bit is 'null' so drop it
    return adcout

#main function
def main():
    # print_message()
    # while True:

    # ch=0を読み取ります。
    # adc_0 = readadc(0)
    adc_0 = random.randint(0, 1023)
    # ch=1を読み取ります。
    # adc_1 = readadc(1)
    adc_1 = random.randint(0, 1023)

    # print ('ch_0 = %d'%(adc_0),end='', flush=True)
    # print (' ch_1 = %d'%(adc_1))

    # 最高速にするには、Sleepをなくす。
    time.sleep(0.2)
    print(adc_0)
    # print(adc_1)

#define a destroy function for clean up everything after the script finished
def destroy():
    #release resource
    GPIO.cleanup()
#
# if run this script directly ,do:
if __name__ == '__main__':
    setup()
    try:
        main()
    #when 'Ctrl+C' is pressed,child program destroy() will be executed.
    except KeyboardInterrupt:
        destroy()

