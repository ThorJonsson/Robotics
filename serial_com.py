#!/usr/bin/python
# -*- coding: utf-8 -*-

import serial


#------------------------ Functions that control communication with serial port


def open_serial(port, baud, timeout):
    ser = serial.Serial(port=port, baudrate=baud, timeout=timeout)
    if ser.isOpen():
        return ser
    else:
        print 'SERIAL ERROR'
		
	
def close(ser):
    ser.close()


# Sends the instruction package to the serial port
def write_data(ser, data):
	# 0xff is always at the start of an instruction package
	data_start = to_hex(0xff)
	data = data_start + data_start + data
    ser.write(data)


def read_data(ser, size=1):
    return ser.read(size)


#------------------ Fundamental functions for constructing instruction packages


def check_sum(data):
	ret = 0
	for w in data:
		ret += ord(w)
	# Why 0xFF????
	return (~(ret))&0xFF


def to_hex(val):
    return chr(val)


def decode_data(data):
    res = ''
    for d in data:
        res += hex(ord(d)) + ' '

    return res


#----------- Functions that construct instruction packages for specific actions


# Before: motor_id hasn't been converted to hex, turn_on acts as a boolean
# After: instruction packet for pinging the motors has been constructed
# To ping a motor with ID 1:
# 0xff 0xff 0x01(ID) 0x02(length) 0x01(instruction) checksum
def ping_motor(motor_id):
	data_id = to_hex(motor_id)
	# data_length is always 2 for pinging
	data_length = to_hex(0x02)
	# for pinging the instruction is always 1
	data_instruction = to_hex(0x01)
	# compute the checksum
	data_checksum = to_hex(check_sum(data))
	# add checksum to the instruction package
	data += data_checksum
	return data


# Before: motor_id hasn't been converted to hex, turn_on acts as a boolean
# After: instruction packet for changing the LED state has been constructed
# To change LED state the following info needs to be sent:
# 0xff 0xff motor_id data_length data_instruction LED_address switch check_sum
def switch_LED(motor_id, turn_on):
	data_id = to_hex(motor_id)
	# data_length is 3 + the number of parameters given to a specific address
	data_length = to_hex(0x04)
	# write is always given by 0x03, switching light is done with write
	data_instruction = to_hex(0x03)
	LED_address = to_hex(0x19)
	
	if turn_on:
		switch = to_hex(0x01)
	else:
		switch = to_hex(0x00)
	
	data = data_id + data_length + data_instruction + LED_address + switch
	# compute the checksum
	data_checksum = to_hex(check_sum(data))
	# add checksum to the instruction package
	data += data_checksum
	return data


if __name__ == '__main__':

	# we open the port
	serial_port = open_serial('/dev/ttyUSB0', 1000000, timeout=0.1)

	# Create an instruction to turn the LED on
	turn_on = 1
	motors = [0x3d,0x3E,0x6]
	for i in motors:
		data_id = to_hex(i)
		data = switch_LED(data_id, turn_on)

		print decode_data(data)
		write_data(serial_port, data)

		# read the status packet (size 6)
		d = read_data(serial_port, 6)
		print decode_data(d)
