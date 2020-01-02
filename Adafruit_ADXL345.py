#!/usr/bin/env python3
from I2C import I2C
from time import sleep
import RPi.GPIO as GPIO
from sys import version_info

if version_info.major == 3:
	raw_input = input

class ADXL345(I2C):

	ADXL345_ADDRESS          = 0x53

	ADXL345_REG_DEVID        = 0x00 # Device ID
	ADXL345_REG_DATAX0       = 0x32 # X-axis data 0 (6 bytes for X/Y/Z)
	ADXL345_REG_POWER_CTL    = 0x2D # Power-saving features control

	ADXL345_DATARATE_0_10_HZ = 0x00
	ADXL345_DATARATE_0_20_HZ = 0x01
	ADXL345_DATARATE_0_39_HZ = 0x02
	ADXL345_DATARATE_0_78_HZ = 0x03
	ADXL345_DATARATE_1_56_HZ = 0x04
	ADXL345_DATARATE_3_13_HZ = 0x05
	ADXL345_DATARATE_6_25HZ  = 0x06
	ADXL345_DATARATE_12_5_HZ = 0x07
	ADXL345_DATARATE_25_HZ   = 0x08
	ADXL345_DATARATE_50_HZ   = 0x09
	ADXL345_DATARATE_100_HZ  = 0x0A # (default)
	ADXL345_DATARATE_200_HZ  = 0x0B
	ADXL345_DATARATE_400_HZ  = 0x0C
	ADXL345_DATARATE_800_HZ  = 0x0D
	ADXL345_DATARATE_1600_HZ = 0x0E
	ADXL345_DATARATE_3200_HZ = 0x0F

	ADXL345_RANGE_2_G        = 0x00 # +/-  2g (default)
	ADXL345_RANGE_4_G        = 0x01 # +/-  4g
	ADXL345_RANGE_8_G        = 0x02 # +/-  8g
	ADXL345_RANGE_16_G       = 0x03 # +/- 16g

	def __init__(self, busnum=-1, debug=False):
		self.accel = I2C(self.ADXL345_ADDRESS, busnum, debug)
		if self.accel.readU8(self.ADXL345_REG_DEVID) == 0xE5:
			# Enable the accelerometer
			self.accel.write8(self.ADXL345_REG_POWER_CTL, 0x08)

	def setRange(self, range):
		# Read the data format register to preserve bits.  Update the data
		# rate, make sure that the FULL-RES bit is enabled for range scaling
		format = ((self.accel.readU8(self.ADXL345_REG_DATA_FORMAT) & ~0x0F) |
		  range | 0x08)
		# Write the register back to the IC
		seld.accel.write8(self.ADXL345_REG_DATA_FORMAT, format)

	def getRange(self):
		return self.accel.readU8(self.ADXL345_REG_DATA_FORMAT) & 0x03

	def setDataRate(self, dataRate):
		# Note: The LOW_POWER bits are currently ignored,
		# we always keep the device in 'normal' mode
		self.accel.write8(self.ADXL345_REG_BW_RATE, dataRate & 0x0F)

	def getDataRate(self):
		return self.accel.readU8(self.ADXL345_REG_BW_RATE) & 0x0F

	# Read the accelerometer
	def read(self):
		raw = self.accel.readList(self.ADXL345_REG_DATAX0, 6)
		print (raw)
		res = []
		for i in range(0, 6, 2):
			g = raw[i] | (raw[i+1] << 8)
			g = 65535 - g
			if g > 32767: 
				g -= 65535
			res.append(g)
		return res

def print_msg():
	print ("========================================")
	print ("|                ADXL345               |")
	print ("|    ------------------------------    |")
	print ("|          SCL connect to SCL          |")
	print ("|          SDA connect to SDA          |")
	print ("|                                      |")
	print ("|        Read value from ADXL345       |")
	print ("|                                      |")
	print ("|                            SunFounder|")
	print ("========================================\n")
	print ("Program is running...")
	print ("Please press Ctrl+C to end the program...")
	raw_input ("Press anykey to begin\n")

# Simple example prints accelerometer data once per second:
def main():
	accel = ADXL345()
	while True:
		x, y, z = accel.read()
		print ("X: %d, Y: %d, Z: %d"%(x, y, z))
		print (" ")
		sleep(1) # Output is fun to watch if this is commented out

def destroy():
	exit()

if __name__ == '__main__':
	try:
		main()
	except KeyboardInterrupt:
		destroy()