#!/usr/bin/env python
import RPi.GPIO as GPIO
import time
from random import randint


# Set up pins
SDI   = 17
RCLK  = 18
SRCLK = 27

TouchPin = 22

# Define a segment code from 0 to 6 in Hexadecimal
SegCode = [0x06, 0x5b, 0x4f, 0x66, 0x6d, 0x7d]

def print_msg():
	print 'Program is running...'
	print 'Please press Ctrl+C to end the program...'

def setup():
	GPIO.setmode(GPIO.BCM)
	GPIO.setup(SDI, GPIO.OUT, initial=GPIO.LOW)
	GPIO.setup(RCLK, GPIO.OUT, initial=GPIO.LOW)
	GPIO.setup(SRCLK, GPIO.OUT, initial=GPIO.LOW)
        GPIO.setup(TouchPin, GPIO.IN, pull_up_down=GPIO.PUD_UP)

# Shift the data to 74HC595
def hc595_shift(dat):
	for bit in range(0, 8):	
		GPIO.output(SDI, 0x80 & (dat << bit))
		GPIO.output(SRCLK, GPIO.HIGH)
		time.sleep(0.001)
		GPIO.output(SRCLK, GPIO.LOW)
	GPIO.output(RCLK, GPIO.HIGH)
	time.sleep(0.001)
	GPIO.output(RCLK, GPIO.LOW)

def loop():
	while True:
            if not GPIO.input(TouchPin):
                 hc595_shift(SegCode[randint(0,5)])
                 time.sleep(2.0)

            hc595_shift(SegCode[randint(0,5)])
            time.sleep(0.060)

def destroy():   #When program ending, the function is executed. 
	GPIO.cleanup()

if __name__ == '__main__': #Program starting from here 
	print_msg()
	setup() 
	try:
		loop()  
	except KeyboardInterrupt:  
		destroy() 
