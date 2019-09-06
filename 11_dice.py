#!/usr/bin/env python3
import RPi.GPIO as GPIO
import time
import random

# Set up pins
SDI   = 17
RCLK  = 18
SRCLK = 27

TouchPin = 22

# Define a segment code from 1 to 6 in Hexadecimal
SegCode = [0x06, 0x5b, 0x4f, 0x66, 0x6d, 0x7d]

# Used to record button press
flag = 0

def print_msg():
	print 'Program is running...'
	print 'Please press Ctrl+C to end the program...'

def setup():
	GPIO.setmode(GPIO.BCM)
	GPIO.setwarnings(False)
	GPIO.setup(SDI, GPIO.OUT, initial=GPIO.LOW)
	GPIO.setup(RCLK, GPIO.OUT, initial=GPIO.LOW)
	GPIO.setup(SRCLK, GPIO.OUT, initial=GPIO.LOW)
	GPIO.setup(TouchPin, GPIO.IN, pull_up_down = GPIO.PUD_UP)
	GPIO.add_event_detect(TouchPin, GPIO.RISING, callback = randomISR, bouncetime = 20)

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

def randomISR(channel):
	global flag
	flag = 1

def destroy():
	GPIO.cleanup()

def main():
	global flag
	print_msg()
	while True:
		num = random.randint(1,6)
		hc595_shift(SegCode[num-1])
		print num, hex(SegCode[num-1])
		if flag == 1:
			print "Num: ", num
			time.sleep(2)
			flag = 0
		else:
			time.sleep(0.01)

if __name__ == '__main__':
	setup()
	try:
		main()
	except KeyboardInterrupt:
		destroy()
