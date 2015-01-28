#!/usr/bin/python
# -*- coding: utf-8 -*-

import serial


def open_serial(port, baud,timeout):
    ser = serial.Serial(port=port, baudrate=baud, timeout=timeout)
    if ser.isOpen():
        return ser
    else:
        print 'SERIAL ERROR'

def check_sum(data):
	ret = 0
	for w in data:
		ret += ord(w)
	return (~(ret))&0xFF
		
	
def close(ser):
    ser.close()


def write_data(ser, data):
    ser.write(data)


def read_data(ser, size=1):
    return ser.read(size)


def to_hex(val):
    return chr(val)


def decode_data(data):
    res = ''
    for d in data:
        res += hex(ord(d)) + ' '

    return res

if __name__ == '__main__':

	# we open the port
	serial_port = open_serial('/dev/ttyUSB0', 1000000, timeout=0.1)

	# we create the packet for a LED ON command
	# two start bytes
	data_start = to_hex(0xff)

	#~ # id of the motor (here 1), you need to change
	#~ data_id = to_hex(0x01)

	# lenght of the packet
	data_lenght = to_hex(0x04)

	# instruction write= 0x03
	data_instruction = to_hex(0x03)

	# instruction parameters
	data_param1 = to_hex(0x19)  # LED address=0x19
	data_param2 = to_hex(0x00)  # write 0x01 = ping the motor

	adress = [0x3d,0x3E,0x6]
	for i in adress:
		data_id = to_hex(i)
		# we concatenate everything
		data = data_start + data_start + data_id + data_lenght + \
		data_instruction + data_param1 + data_param2 
		
		data_second = data_id + data_lenght + data_instruction + data_param1 + data_param2
		
		# checksum (read the doc)
		
		data_checksum = to_hex(check_sum(data_second))

		data += data_checksum


		print decode_data(data)
		write_data(serial_port, data)

		# read the status packet (size 6)
		d = read_data(serial_port, 6)
		print decode_data(d)
