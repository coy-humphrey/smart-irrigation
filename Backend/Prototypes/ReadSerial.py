#!/usr/bin/python

import serial
import time
import datetime
import ConfigParser
import sys
import select

def get_devices():
	config = ConfigParser.RawConfigParser( )
	config.read( 'serial_devices.ini' )
	results = {}
	for device in config.options('devices'):
		if config.get ('devices', device).lower() == "serial":
			stream = serial.Serial(device, 9600)
		else:
			stream = sys.stdin
		results[stream] = [x.strip() for x in config.get('format', device).split(',')]
	return results

def parseLine (device, device_dict):
	line = device.readline()
	# In future iterations, this should cause some sort of error message and possibly an attempt to reconnect.
	if not line: 
		return False
	# Devices give a tab separated list of sensor readings not including time
	# So we generate the time
	curr_time = datetime.datetime.today().strftime('%Y-%m-%d %H:%M:%S')
	# We pull the sensor readings from the input and throw them in a list with time
	results = [curr_time] + line.strip().split('\t')
	# We get the row names of the sensors and append them to "time" the name of the time row
	fields = ["time"] + device_dict[device]
	# Then we put the readings in a dictionary with the row names as keys
	results = dict(zip(fields, results))
	# For now we print the dictionary, in the future we will push it to DB
	print results
	# Returning true tells the calling function that this stream is still open
	return True

def main():
    device_dict = get_devices()
    devices = device_dict.keys()

    # While there are still open streams
    while devices:
    	# Wait for a stream to have data ready
    	readable, _, _ = select.select(devices, [], [])
    	# Then, parse a line from each ready stream. If a stream is closed, remove it from list
    	devices = [x for x in readable if parseLine(x, device_dict)]


if __name__ == '__main__':
    main()
