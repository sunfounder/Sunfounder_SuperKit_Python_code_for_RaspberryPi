#!/usr/bin/env python
import RPi.GPIO as GPIO
import time

SDI   = 11
RCLK  = 12
SRCLK = 13

code_H = [0x01,0xff,0x80,0xff,0x01,0x02,0x04,0x08,0x10,0x20,0x40,0x80,0xff,0xff,0xff,0xff,0xff,0xff,0xff,0xff]
code_L = [0x00,0x7f,0x00,0xfe,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0xfe,0xfd,0xfb,0xf7,0xef,0xdf,0xbf,0x7f]


def print_msg():
	print 'Program is running...'
	print 'Please press Ctrl+C to end the program...'

def setup():
	GPIO.setmode(GPIO.BOARD)    # Number GPIOs by its physical location
	GPIO.setup(SDI, GPIO.OUT)
	GPIO.setup(RCLK, GPIO.OUT)
	GPIO.setup(SRCLK, GPIO.OUT)
	GPIO.output(SDI, GPIO.LOW)
	GPIO.output(RCLK, GPIO.LOW)
	GPIO.output(SRCLK, GPIO.LOW)

def hc595_in(dat):
	for bit in range(0, 8):	
		GPIO.output(SDI, 0x80 & (dat << bit))
		GPIO.output(SRCLK, GPIO.HIGH)
		time.sleep(0.001)
		GPIO.output(SRCLK, GPIO.LOW)

def hc595_out():
	GPIO.output(RCLK, GPIO.HIGH)
	time.sleep(0.001)
	GPIO.output(RCLK, GPIO.LOW)


def loop():
	while True:
		for i in range(0, len(code_H)):
			hc595_in(code_L[i])
			hc595_in(code_H[i])
			hc595_out()
			time.sleep(0.1)

		for i in range(len(code_H)-1, -1, -1):
			hc595_in(code_L[i])
			hc595_in(code_H[i])
			hc595_out()
			time.sleep(0.1)

def destroy():   # When program ending, the function is executed. 
	GPIO.cleanup()

if __name__ == '__main__':   # Program starting from here 
	print_msg()
	setup() 
	try:
		loop()  
	except KeyboardInterrupt:  
		destroy()  
