#!/usr/bin/python
from gpiozero import LED, Button
import RPi.GPIO as GPIO
import time
from random import uniform
from enum import Enum
#2 + 5V
#4 - 5V
#6 + gnd
#8 - gp14
#10 - gp15 
#12 - gp18 
#14 - gnd
#16 - gp23 

#1 3v3
#3 gp2
#5 gp3
#7 + gp4 -> trigger
#9 gnd
#11 + gp17 -> echo
#13 gp27

PULSES_SPEED = 17150


def calculateDistance(timeBegin, timeEnd):
    return round((timeEnd - timeBegin) * PULSES_SPEED, 2)

try:
    #prepare
    GPIO.setmode(GPIO.BOARD)

    PIN_TRIGGER = 7
    PIN_ECHO = 11

    GPIO.setup(PIN_TRIGGER, GPIO.OUT)
    GPIO.setup(PIN_ECHO, GPIO.IN)

    GPIO.output(PIN_TRIGGER, GPIO.LOW)

    print("wait for settle")
    time.sleep(2)

    print("activitate sensor")
    GPIO.output(PIN_TRIGGER, GPIO.HIGH)
    time.sleep(0.000001)
    GPIO.output(PIN_TRIGGER, GPIO.LOW)


    while GPIO.input(PIN_ECHO) == 0:
        pulse_start = time.time()
    
    while GPIO.input(PIN_ECHO) == 1:
        pulse_end = time.time()
    
    dist = calculateDistance(pulse_start, pulse_end)
    print("dist: %s" % dist)
finally:
    GPIO.cleanup()