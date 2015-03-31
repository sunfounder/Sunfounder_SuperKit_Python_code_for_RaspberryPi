#!/usr/bin/env python
import RPi.GPIO as GPIO

SigPin = 11    # pin11

g_count = 0

def count(ev=None):
	global g_count
	g_count += 1

def setup():
	GPIO.setmode(GPIO.BOARD)       # Numbers GPIOs by physical location
	GPIO.setup(SigPin, GPIO.IN, pull_up_down=GPIO.PUD_UP)    # Set Pin's mode is input, and pull up to high level(3.3V)
	GPIO.add_event_detect(SigPin, GPIO.RISING, callback=count) # wait for rasing

def loop():
	while True:
		print 'g_count = %d' % g_count

def destroy():
	GPIO.cleanup()    # Release resource

if __name__ == '__main__':     # Program start from here
	setup()
	try:
		loop()
	except KeyboardInterrupt:  # When 'Ctrl+C' is pressed, the child program destroy() will be  executed.
		destroy()

