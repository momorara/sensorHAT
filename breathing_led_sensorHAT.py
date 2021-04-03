#!/usr/bin/python
"""
breathing_led_sensorHAT.py -LED 22 -start 0 -step 5 -stop 6

2021/03/25  プログラム起動時に設定値を渡せるようにした。
2021/03/27  微修正
2021/03/29  stopカウンターを追加


scp -r sensorHAT pi@192.168.68.126:/home/pi
scp -r sensorHAT/*.py pi@192.168.68.126:/home/pi/sensorHAT

scp -r sensorHAT/*.py pi@172.20.10.6:/home/pi/sensorHAT
"""

import RPi.GPIO as GPIO
import time
import argparse

p = argparse.ArgumentParser()
p.add_argument("-LED_pin",  help="led pin number"  ,   type=int, default= 17)
p.add_argument("-start"  ,  help="start duty cycle",   type=int, default= 0)
p.add_argument("-step"   ,  help="duty cycle step" ,   type=int, default= 4)
p.add_argument("-stop_n" ,  help="stop count n"    ,   type=int, default= 5)
args = p.parse_args()

LEDPIN = args.LED_pin
# pinは17,26,2７のみ指定できる
if LEDPIN not in (17,26,27):
    print('error')
    # LEDPIN = 5

start_duty_cycle = args.start
if start_duty_cycle < 0 or start_duty_cycle > 100:
    print('error')
    start_duty_cycle = 0

duty_cycle_step  = args.step
if duty_cycle_step < 1 or duty_cycle_step > 100:
    print('error')
    duty_cycle_step = 4

stop_n = args.stop_n

print('LED pin =',LEDPIN,' start =',start_duty_cycle,' step =',duty_cycle_step,' stop_count =',stop_n)


#set BCM_GPIO 18(GPIO1) as LED pin
iR_LED = '22' # iR用なので注意


#print message at the begining ---custom function
def print_message():
    print ('Program is start')

#setup function for some setup---custom function
def setup():
    global p
    GPIO.setwarnings(False)
    #set the gpio modes to BCM numbering
    GPIO.setmode(GPIO.BCM)
    #set all LedPin's mode to output,and initial level to HIGH(3.3V)
    GPIO.setup(LEDPIN,GPIO.OUT,initial=GPIO.LOW)
    #set LEDPIN as PWM output,and frequency=100Hz
    p = GPIO.PWM(LEDPIN,100)
    #set p begin with ualue 0
    p.start(0)

#main function
def main():
    #print info
    print_message()
    # print('LED pin =',LEDPIN,' start =',start_duty_cycle,' step =',duty_cycle_step,' stop_count =')
    # print('LED pin =',LEDPIN,' start =',start_duty_cycle,' step =',duty_cycle_step,' stop_count =',stop_n)
    n = stop_n
    while n > 0:
        print(">>   点灯 duty cycle  ")
        #increase duty cycle from 0 to 100
        for dc in range(start_duty_cycle,101,duty_cycle_step):
            #chang duty cycle to dc
            p.ChangeDutyCycle(dc)
            time.sleep(0.1)
        p.ChangeDutyCycle(100)
        time.sleep(0.5)
        print(">>   消灯 duty cycle   ")
        #decrease duty cycle from 100 to 0
        for dc in range(100,-1,-duty_cycle_step):
            #change duty cycle to dc
            p.ChangeDutyCycle(dc)
            time.sleep(0.1)
        p.ChangeDutyCycle(0)
        time.sleep(0.7)
        n = n -1 


#define a destroy function for clean up everything after the script finished
def destroy():
    #stop p
    p.stop()
    #turn off led
    GPIO.output(LEDPIN,GPIO.LOW)
    #release resource
    GPIO.cleanup()
    pass

# if run this script directly ,do:
if __name__ == '__main__':
    setup()
    try:
        main()
    #when 'Ctrl+C' is pressed,child program destroy() will be executed.
    except KeyboardInterrupt:
        destroy()
        pass
    pass
