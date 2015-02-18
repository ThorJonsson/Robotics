import itertools
import time
import numpy
import pypot.dynamixel
import math

# Before: We assume we've not scanned the motors as we'd like to run this     # function only at the beginning of each session. Therefore it makes no sense # to not include it in this function.
# After: We've scanned the motors and renamed them 
def change_motorid(found_ids,dxl_io):
    # We can scan the motors
    #found_ids = dxl_io.scan()#   this may take several seconds
    # It is essential to know the current labels to prevent from making errors
	print 'Detected:', found_ids
    
    # This loop goes through all the motors and asks the user to relabel
	for motor_id in found_ids:
		print "When labelling the motors please do not use any of the already detected ones as it will produce an error!"
		# Lights up the motor 
		print "********"
		print type(motor_id)
		print "********"
		dxl_io.switch_led_on(motor_id)
		# I think it is only possible to use integers but I can't find any    # documentation
		new_id = int(input("Please enter an integer to label the lit motor"))
		dxl_io.change_id({motor_id : new_id})
	# To check whether everything went according to plan    
	found_ids = dxl_io.scan()
	print "The new id's are: ", found_ids

def leg_ik(x3,y3,z3,alpha = 20.69, beta = 5.06,l1=51,l2=63.7,l3=93):
	d13 = math.sqrt(x3*x3 + y3*y3) - l1
	d = math.sqrt(d13*d13 + z3*z3)
	tmp = (l2*l2 + d*d - l3*l3)/(2*l2*d)
	a1 = z3 / d13
	a2 = (l2*l2 + l3*l3 - d*d)/(2*l2*l3)
	#~ print a2
	#~ print a1
	#~ print tmp
	angles = (None,None,None)
	theta1 = math.degrees(math.atan2(y3,x3))
	theta2 = math.degrees(math.atan(a1) + math.acos(tmp))
	theta3 = 180 - math.degrees(math.acos(a2))
	# Corrections to the angles theta2 and theta3
	theta2 = theta2 + alpha
	theta3 = -(theta3 - 90 + alpha + beta)
	angles = (theta1,theta2,theta3)
	return angles  
  
if __name__ == '__main__':
    # we first open the Dynamixel serial port
	with pypot.dynamixel.DxlIO('/dev/ttyUSB0', baudrate=1000000) as dxl_io:   
		found_ids = [1, 2, 3]#dxl_io.scan()
		print "-----------------------------"
		print found_ids
		print "-----------------------------"
		#change_motorid(found_ids,dxl_io)
		# we power on the motors
		dxl_io.enable_torque(found_ids)
		# we get the current positions
		print 'Current pos:', dxl_io.get_present_position(found_ids)
		pos = {found_ids[0] : 0,found_ids[1] : 0,found_ids[2] : 0}
		#print 'Cmd:', pos
		#~ T = time.time()
		# This moves it to the set position
		dxl_io.set_goal_position(pos)
		time.sleep(1)


		position = dxl_io.get_present_position(found_ids)
		# Angles that correspond to current position
		print leg_ik(position[0],position[1],position[2])
		# we get the current positions
		print 'New pos:', dxl_io.get_present_position(found_ids)
		# we power off the motors
		dxl_io.disable_torque(found_ids)
		
		time.sleep(1)  # we wait for 1s
