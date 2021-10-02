#! /usr/bin/env python3
# -*- coding: utf-8 -*-
# ## #############################################################
#
# Author: Mauricio Matamoros
# Date:
#
# ## ############################################################
import smbus
import struct
import time

DESIRED_TEMPERATURE = 50.0
MAX_POWER = 100.0
# Define thresholds:
ONTHRES = DESIRED_TEMPERATURE - 10
OFFTHRES = DESIRED_TEMPERATURE + 5

# Arduino's I2C device address
SLAVE_ADDR = 0x0A # I2C Address of Arduino 1

# Initialize the I2C bus;
# RPI version 1 requires smbus.SMBus(0)
i2c = smbus.SMBus(1)

def readTemperature():
	try:
		# Creates a message object to read 4 bytes from SLAVE_ADDR
		msg = smbus2.i2c_msg.read(SLAVE_ADDR, 4)
		i2c.i2c_rdwr(msg)  # Performs write
		data = list(msg)   # Converts stream to list
		temp = struct.unpack('<f', ''.join([chr(c) for c in data]))
		# print('Received temp: {} = {}'.format(data, temp))
		return temp
	except:
		return None

def writePower(pwr):
	try:
		data = struct.pack('<f', pwr) # Packs number as float
		# Creates a message object to write 4 bytes from SLAVE_ADDR
		msg = smbus2.i2c_msg.write(SLAVE_ADDR, data)
		i2c.i2c_rdwr(msg)  # Performs write
	except:
		pass

def main():
	print("-= On/Off controller =-")
	print("  Desired temperature: {:0.2f}°C".format(DESIRED_TEMPERATURE))

	while True:
		try:
			# Read and report current temperature
			current = readTemperature()
			print("\r  Current temperature: {:0.2f}°C".format(current), end="")

			# If temperature is lower than on threshold, turn on (MAX power).
			if current <= ONTHRES:
				writePower(MAX_POWER)
			# If temperature is greater than off threshold, turn off.
			elif current >= OFFTHRES:
				writePower(0)
			# 1 sec so controller can act.
			sleep(1)
		except:
			print("\tError!")
			writePower(0)

if __name__ == '__main__':
	main()
