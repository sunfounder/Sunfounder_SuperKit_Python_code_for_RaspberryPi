#!/usr/bin/env python3
import RPi.GPIO as GPIO
import time

pins = [17, 18, 27, 22, 23, 24, 25, 4]

def setup():
	GPIO.setmode(GPIO.BCM)        # Numbers GPIOs by BCM
	for pin in pins:
		GPIO.setup(pin, GPIO.OUT)   # Set all pins' mode is output
		GPIO.output(pin, GPIO.HIGH) # Set all pins to high(+3.3V) to off led

def loop():
	while True:
		for pin in pins:
			GPIO.output(pin, GPIO.LOW)	
			time.sleep(0.05)
			GPIO.output(pin, GPIO.HIGH)
		for pin in reversed(pins):
			GPIO.output(pin, GPIO.LOW)
			time.sleep(0.05)
			GPIO.output(pin, GPIO.HIGH)

def destroy():
	for pin in pins:
		GPIO.output(pin, GPIO.HIGH)    # turn off all leds
	GPIO.cleanup()                     # Release resource

if __name__ == '__main__':     # Program start from here
	setup()
	try:
		loop()
	except KeyboardInterrupt:  # When 'Ctrl+C' is pressed, the child program destroy() will be  executed.
		destroy()

