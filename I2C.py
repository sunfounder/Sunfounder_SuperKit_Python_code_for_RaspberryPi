#!/usr/bin/python3

import smbus

class I2C(object):

  RPI_REVISION_0 = ["900092","900093", "920093",]
  RPI_REVISION_1_MODULE_B = ["Beta", "0002", "0003", "0004", "0005", "0006", "000d", "000e", "000f"]
  RPI_REVISION_1_MODULE_A = ["0007", "0008", "0009",]
  RPI_REVISION_1_MODULE_BP = ["0010", "0013","900032"]
  RPI_REVISION_1_MODULE_AP = ["0012","900021"]
  RPI_REVISION_2 = ["a01041", "a21041","a22042"]
  RPI_REVISION_3 = ["a02082", "a22082","a32082"]
  RPI_REVISION_3_MODULE_BP = ["a020d3"]
  RPI_REVISION_3_MODULE_AP = ["9020e0"]
  RPI_REVISION_4 = ["a03111", "b03111", "c03111"]

  def _get_bus_number(self):
    "Gets the version number of the Raspberry Pi board"
    # Courtesy quick2wire-python-api
    # https://github.com/quick2wire/quick2wire-python-api
    # Updated revision info from: http://elinux.org/RPi_HardwareHistory#Board_Revision_History
    try:
      f = open('/proc/cpuinfo','r')
      for line in f:
        if line.startswith('Revision'):
          if line[11:-1] in self.RPI_REVISION_0:
            return 0
          elif line[11:-1] in self.RPI_REVISION_1_MODULE_B:
            return 0
          elif line[11:-1] in self.RPI_REVISION_1_MODULE_A:
            return 0
          elif line[11:-1] in self.RPI_REVISION_1_MODULE_BP:
            return 1
          elif line[11:-1] in self.RPI_REVISION_1_MODULE_AP:
            return 0
          elif line[11:-1] in self.RPI_REVISION_2:
            return 1
          elif line[11:-1] in self.RPI_REVISION_3:
            return 1
          elif line[11:-1] in self.RPI_REVISION_3_MODULE_BP:
            return 1
          elif line[11:-1] in self.RPI_REVISION_3_MODULE_AP:
            return 1
          elif line[11:-1] in self.RPI_REVISION_4:
            return 1
          else:
            return line[11:-1]
    except Exception as e:
      f.close()
      return e
    finally:
      f.close()

  def __init__(self, address, bus_number=-1, debug=False):
    self.address = address
    # By default, the correct I2C bus is auto-detected using /proc/cpuinfo
    # Alternatively, you can hard-code the bus version below:
    # self.bus = smbus.SMBus(0); # Force I2C0 (early 256MB Pi's)
    # self.bus = smbus.SMBus(1); # Force I2C1 (512MB Pi's)
    if bus_number == -1:
      self.bus_number = self._get_bus_number()
    else:
      self.bus_number = bus_number
    #print (self.bus_number)
    self.bus = smbus.SMBus(self.bus_number)
    self.debug = debug

  def reverseByteOrder(self, data):
    "Reverses the byte order of an int (16-bit) or long (32-bit) value"
    # Courtesy Vishal Sapre
    byteCount = len(hex(data)[2:].replace('L','')[::2])
    val       = 0
    for i in range(byteCount):
      val    = (val << 8) | (data & 0xff)
      data >>= 8
    return val

  def errMsg(self):
    print ("Error accessing 0x%02X: Check your I2C address" % self.address)
    return -1

  def write8(self, reg, value):
    "Writes an 8-bit value to the specified register/address"
    try:
      self.bus.write_byte_data(self.address, reg, value)
      if self.debug:
        print ("I2C: Wrote 0x%02X to register 0x%02X" % (value, reg))
    except IOError as err:
      return self.errMsg()

  def write16(self, reg, value):
    "Writes a 16-bit value to the specified register/address pair"
    try:
      self.bus.write_word_data(self.address, reg, value)
      if self.debug:
        print ("I2C: Wrote 0x%02X to register pair 0x%02X,0x%02X" %(value, reg, reg+1))
    except IOError as err:
      return self.errMsg()

  def writeRaw8(self, value):
    "Writes an 8-bit value on the bus"
    try:
      self.bus.write_byte(self.address, value)
      if self.debug:
        print ("I2C: Wrote 0x%02X" % value)
    except IOError as err:
      return self.errMsg()

  def writeList(self, reg, list):
    "Writes an array of bytes using I2C format"
    try:
      if self.debug:
        print ("I2C: Writing list to register 0x%02X:" % reg)
        print (list)
      self.bus.write_i2c_block_data(self.address, reg, list)
    except IOError as err:
      return self.errMsg()

  def readList(self, reg, length):
    "Read a list of bytes from the I2C device"
    try:
      results =self.bus.read_i2c_block_data(self.address, reg, length)
      if self.debug:
        print ("I2C: Device 0x%02X returned the following from reg 0x%02X" %(self.address, reg))
        print (results)
      return results
    except IOError as err:
      return self.errMsg()

  def readU8(self, reg):
    "Read an unsigned byte from the I2C device"
    try:
      result = self.bus.read_byte_data(self.address, reg)
      if self.debug:
        print ("I2C: Device 0x%02X returned 0x%02X from reg 0x%02X" %(self.address, result & 0xFF, reg))
      return result
    except IOError as err:
      return self.errMsg()

  def readS8(self, reg):
    "Reads a signed byte from the I2C device"
    try:
      result = self.bus.read_byte_data(self.address, reg)
      if result > 127: result -= 256
      if self.debug:
        print ("I2C: Device 0x%02X returned 0x%02X from reg 0x%02X" %(self.address, result & 0xFF, reg))
      return result
    except IOError as err:
      return self.errMsg()

  def readU16(self, reg, little_endian=True):
    "Reads an unsigned 16-bit value from the I2C device"
    try:
      result = self.bus.read_word_data(self.address,reg)
      # Swap bytes if using big endian because read_word_data assumes little 
      # endian on ARM (little endian) systems.
      if not little_endian:
        result = ((result << 8) & 0xFF00) + (result >> 8)
      if (self.debug):
        print ("I2C: Device 0x%02X returned 0x%04X from reg 0x%02X" % (self.address, result & 0xFFFF, reg))
      return result
    except IOError as err:
      return self.errMsg()

  def readS16(self, reg, little_endian=True):
    "Reads a signed 16-bit value from the I2C device"
    try:
      result = self.readU16(reg,little_endian)
      if result > 32767: result -= 65536
      return result
    except IOError as err:
      return self.errMsg()

if __name__ == '__main__':
  try:
    bus = I2C(address = 0x53, debug = True)
    print ("Default I2C bus is accessible")
  except:
    print ("Error accessing default I2C bus")
