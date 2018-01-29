#!/usr/bin/env python
#================================================
#
#	This program is for SunFounder SuperKit for Rpi.
#	or for the Velleman VMS-502
#
#	Extend use of 8 LED with 74HC595.
#
#	Change the	WhichLeds and sleeptime value under
#	loop() function to change LED mode and speed.
#
#=================================================

import RPi.GPIO as GPIO		#if you use a standard Raspberry PI
#import RTk.GPIO as GPIO	#if you use a RTk.GPIO USB Board for PC or Mac
#import ASUS.GPIO as GPIO	#if you use a ASUS TinkerBoard
import time
import sys			#for displaying without newline

#Datasheet: http://www.ti.com/lit/ds/symlink/sn74hc595.pdf

#name = GPIO Pin
SDI   = 11	#75hc595 PIN 14: Serial Data IN
RCLK  = 12	#74hc595 PIN 12: storage Register CLocK
SRCLK = 13	#74hc595 PIN 11: Shift Register CLocK

#===============   LED Mode Defne ================
#	You can define yourself, in binay, and convert it to Hex 
#	8 bits a group, 0 means off, 1 means on
#	like : 0101 0101, means LED1, 3, 5, 7 are on.(from left to right)
#	and convert to 0x55.

LED0 = [0x01,0x02,0x04,0x08,0x10,0x20,0x40,0x80]	#original mode
LED1 = [0x01,0x03,0x07,0x0f,0x1f,0x3f,0x7f,0xff]	#blink mode 1
LED2 = [0x01,0x05,0x15,0x55,0xb5,0xf5,0xfb,0xff]	#blink mode 2
LED3 = [0x02,0x03,0x0b,0x0f,0x2f,0x3f,0xbf,0xff]	#blink mode 3
#=================================================

def print_msg():
	print 'Program is running...'
	print 'Please press Ctrl+C to end the program...'


def setup():
	GPIO.setmode(GPIO.BOARD)	# Number GPIOs by its physical location
	GPIO.setup(SDI, GPIO.OUT)	# Define Pin as OUTPUT
	GPIO.setup(RCLK, GPIO.OUT)	# Define Pin as OUTPUT
	GPIO.setup(SRCLK, GPIO.OUT)	# Define Pin as OUTPUT
	GPIO.output(SDI, GPIO.LOW)	# Set Pin to 0
	GPIO.output(RCLK, GPIO.LOW)	# Set Pin to 0
	GPIO.output(SRCLK, GPIO.LOW)	# Set Pin to 0


#write as Serial Bits to HC595 by waking bitwise through the byte

def hc595_in(dat):
	sys.stdout.write( "\r" + '{:08b}'.format(dat) )	# display on screen
	sys.stdout.flush()				#
	sys.stdout.write( "\n" )			#
	sys.stdout.flush()				#
	for bit in range(0, 8):
		GPIO.output(SDI, 0x80 & (dat << bit))	#<< is the bitwise shift operator
		GPIO.output(SRCLK, GPIO.HIGH)
		time.sleep(0.1)
		sys.stdout.write( "x" )			#
		sys.stdout.flush()			# display on screen
		GPIO.output(SRCLK, GPIO.LOW)


#send an impulse to RCLK that will load the data from the Shift Register in the Chip to the Display Register in the Chip

def hc595_out():	#pin 12: storage Register CLocK
	GPIO.output(RCLK, GPIO.HIGH)
	time.sleep(0.001)
	GPIO.output(RCLK, GPIO.LOW)
	sys.stdout.write( " (X) Loading to DisplayRegister ")
	sys.stdout.flush()


def loop():
	WhichLeds = LED0	# Change Mode, modes from LED0 to LED3
	sleeptime = 1		# Change speed, lower value, faster speed
	while True:
		#walk from bit 1 to bit 8
		for i in range(0, len(WhichLeds)):
			#write data serial to 74hc595
			hc595_in(WhichLeds[i])
			#adopt the data in the shift register
			hc595_out()
			time.sleep(sleeptime)
		
		#reverse direction
		for i in range(len(WhichLeds)-1, -1, -1):
			hc595_in(WhichLeds[i])
			hc595_out()
			time.sleep(sleeptime)


def destroy():   # When program ending, the function is executed. 
	GPIO.cleanup()

if __name__ == '__main__': # Program starting from here 
	print_msg()
	setup() 
	try:
		loop()  
	except KeyboardInterrupt:  
		destroy()  
