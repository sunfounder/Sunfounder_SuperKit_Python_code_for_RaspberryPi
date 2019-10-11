#!/usr/bin/env python3
import RPi.GPIO as GPIO
import time

LedPin = 17

def setup():
	GPIO.setmode(GPIO.BCM)       # Numbers GPIOs by BCM
	GPIO.setup(LedPin, GPIO.OUT)   # Set LedPin's mode is output
	GPIO.output(LedPin, GPIO.HIGH) # Set LedPin high(+3.3V) to off led

def loop():
	while True:
		print ("...led on")
		GPIO.output(LedPin, GPIO.LOW)  # led on
		time.sleep(0.5)
		print ("led off...")
		GPIO.output(LedPin, GPIO.HIGH) # led off
		time.sleep(0.5)

def destroy():
	GPIO.output(LedPin, GPIO.HIGH)     # led off
	GPIO.cleanup()                     # Release resource

if __name__ == '__main__':     # Program start from here
	setup()
	try:
		loop()
	except KeyboardInterrupt:  # When 'Ctrl+C' is pressed, the child program destroy() will be  executed.
		destroy()

