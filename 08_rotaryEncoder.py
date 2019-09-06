#!/usr/bin/env python3

import RPi.GPIO as GPIO
import time

# Set up pins
# Rotary A Pin
RoAPin = 17
# Rotary B Pin
RoBPin = 18
# Rotary Switch Pin
RoSPin = 27

def setup():
	global counter
	global Last_RoB_Status, Current_RoB_Status
	GPIO.setmode(GPIO.BCM)
	GPIO.setup(RoAPin, GPIO.IN)
	GPIO.setup(RoBPin, GPIO.IN)
	GPIO.setup(RoSPin,GPIO.IN, pull_up_down=GPIO.PUD_UP)
	# Set up a falling edge detect to callback clear
	GPIO.add_event_detect(RoSPin, GPIO.FALLING, callback=clear)

	# Set up a counter as a global variable
	counter = 0
	Last_RoB_Status = 0
	Current_RoB_Status = 0

# Define a function to deal with rotary encoder
def rotaryDeal():
	global counter
	global Last_RoB_Status, Current_RoB_Status

	flag = 0
	Last_RoB_Status = GPIO.input(RoBPin)
	# When RoAPin level changes
	while(not GPIO.input(RoAPin)):
		Current_RoB_Status = GPIO.input(RoBPin)
		flag = 1
	if flag == 1:
		# Reset flag
		flag = 0
		if (Last_RoB_Status == 0) and (Current_RoB_Status == 1):
			counter = counter + 1
		if (Last_RoB_Status == 1) and (Current_RoB_Status == 0):
			counter = counter - 1
		print ("counter = %d" % counter)

# Define a callback function on switch, to clean "counter"
def clear(ev=None):
	global counter
	counter = 0

def main():
	while True:
		rotaryDeal()

def destroy():
	# Release resource
	GPIO.cleanup()  

# If run this script directly, do:
if __name__ == '__main__':
	setup()
	try:
		main()
	# When 'Ctrl+C' is pressed, the child program 
	# destroy() will be  executed.
	except KeyboardInterrupt:
		destroy()