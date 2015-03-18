import itertools
import time
import numpy
from pypot.dynamixel import autodetect_robot
import pypot.dynamixel
import math
import json
import time
from contextlib import closing

import pypot.robot

asterix = None


def leg_ik(x3,y3,z3,alpha = 20.69, beta = 5.06,l1=51,l2=63.7,l3=93):
	d13 = math.sqrt(x3*x3 + y3*y3) - l1
	d = math.sqrt(d13*d13 + z3*z3)
	tmp = (l2**2 + d**2 - l3**2)/(2*l2*d)
	a1 = z3 / d13
	a2 = (l2**2 + l3**2 - d**2)/(2*l2*l3)
	
	angles = (None,None,None)
	theta1 = math.degrees(math.atan2(y3,x3))   # OK

	theta2 = math.degrees(math.atan(a1) + math.acos(tmp)) 
	theta3 = 180 - math.degrees(math.acos(a2))
	# Corrections to the angles theta2 and theta3
	theta2 = -(theta2 + alpha)
	theta3 = -(theta3 - 90 + alpha + beta)
	angles = (theta1,theta2,theta3)
	return angles 

def detection():

	my_robot = autodetect_robot() #detect al the legs of the robot. Might take a while to operate.

	#write the configuration found into a json file. We shouldn't use the complete detection whith this json file.
	config = my_robot.to_config()
	with open('my_robot.json', 'wb') as f:
	    json.dump(config, f)

	with closing(pypot.robot.from_json('my_robot.json')) as my_robot:
	    # do stuff without having to make sure not to forget to close my_robot!
	    pass


def initialize():

	asterix = pypot.robot.from_json('my_robot.json')
	# print asterix
	# Note that all these calls will return immediately,
	# and the orders will not be directly sent
	# (they will be sent during the next write loop iteration).
	for m in asterix.motors:
	    print m.present_position
	    m.compliant = False		# <=> enable_torque.
	    m.goal_position = 0

  	# with closing(pypot.robot.from_json('my_robot.json')) as my_robot:
	  #   # do stuff without having to make sure not to forget to close my_robot!
	  #   pass



	time.sleep(2)
	return asterix

def motion(asterix):
	# Do the sinusoidal motions for 10 seconds
	amp = 30
	freq = 0.5
	t0 = time.time()

	while True:
		t = time.time() - t0

		if t > 10:
			break

		pos = amp * numpy.sin(2 * numpy.pi * freq * t)

		asterix.motor_51.goal_position = pos

	    # In order to make the other sinus more visible,
	    # we apply it with an opposite phase and we increase the amplitude.
		asterix.motor_41.goal_position = -1.5 * asterix.motor_51.present_position

	    # We want to run this loop at 50Hz.
		time.sleep(0.02)

def move_leg(x,y,z,leg):
	i=0
	tupl = leg_ik(x,y,z)
	for m in leg:
		# time.sleep(0.1)
		m.goal_position = tupl[i]
		i+=1


def experimentation(asterix):
	tupl = leg_ik(100,0,0)
	asterix.motor_41.goal_position = tupl[0]
	asterix.motor_42.goal_position = tupl[1]
	asterix.motor_43.goal_position = tupl[2]
	time.sleep(0.5)
	tupl = leg_ik(100,-50,-110)
	asterix.motor_41.goal_position = tupl[0]
	asterix.motor_42.goal_position = tupl[1]
	asterix.motor_43.goal_position = tupl[2]

	asterix.close()

def moving_all_legs(asterix,x,y,z,legs):
	tupl = leg_ik(x,y,z)
	move_leg(x,y,z,legs[0])
	move_leg(x,y,z,legs[2])
	move_leg(x,y,z,legs[1])
	move_leg(x,y,z,legs[3])
	move_leg(x,y,z,legs[5])
	move_leg(x,y,z,legs[4])

# detection()
obj = initialize()
# experimentation(obj)
# motion(obj)
legs = [obj.leg1,obj.leg2,obj.leg3,obj.leg4,obj.leg5,obj.leg6]
# moving_all_legs(obj,100,30,-110,legs)
# time.sleep(1)
# for m in obj.motors:
	# m.goal_position = 0
	# time.sleep(0.5)
# time.sleep(1)

move_leg(100,0,-60,legs[0])
move_leg(100,0,-60,legs[3])
move_leg(100,30,-60,legs[5])
move_leg(100,-30,-60,legs[4])
move_leg(100,30,-60,legs[2])
move_leg(100,-30,-60,legs[1])
time.sleep(3)
while 1:
	move_leg(110,-15,-60,legs[0])
	move_leg(110,15,-60,legs[3])
	move_leg(85,30,-60,legs[5])
	move_leg(85,-30,-60,legs[4])
	move_leg(115,30,-60,legs[2])
	move_leg(115,-30,-60,legs[1])
	time.sleep(0.2)

	move_leg(110,15,-70,legs[0])
	move_leg(110,-15,-70,legs[3])
	move_leg(115,30,-60,legs[5])
	move_leg(115,-30,-60,legs[4])
	move_leg(85,30,-60,legs[2])
	move_leg(85,-30,-60,legs[1])
	time.sleep(0.2)

obj.close()
# move_leg(100,50,-110,legs[0])
# move_leg(100,-50,-110,legs[1])
# move_leg(100,50,-110,legs[2])
# move_leg(100,50,-110,legs[3])
# move_leg(100,50,-110,legs[4])
# move_leg(100,-50,-110,legs[5])
