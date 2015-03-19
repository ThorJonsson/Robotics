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
legs = []

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

def get_legs(obj):
	return [obj.leg1,obj.leg2,obj.leg3,obj.leg4,obj.leg5,obj.leg6]

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

def spider_position(x,y,z,asterix):

	i = 1

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
# Before the center is in (0,0,-60)

def romantic_walk(asterix,x,y,z):
	breaklength = 0.2
	# position 1
	#moving_center(asterix,0,-40,-60,legs)
	# position 2
	#moving_center(asterix,0,0,-60,legs)
	# position 3
	# How does the center move?
	# TODO: define steplengths for each of the legs
	moving_center(asterix,x,y,z,legs)
	# position 4 we lift legs 1 and 4
	move_leg(100,0,z + 10,legs[0])
	move_leg(100,0,z + 10,legs[3])
	time.sleep(breaklength)
	# position 5 we put legs 1 and 4 down so that they are perpendicular to the y axis
	move_leg(100,0,z,legs[0])
	move_leg(100,0,z,legs[3])
	time.sleep(breaklength)
	# position 6 we lift up legs 5 and 6
	move_leg(100,30,z + 10,legs[4])	
	move_leg(100,-30,z + 10,legs[5])
		#position 7 put legs 2 and 3 in the air
	move_leg(100,30,z + 10,legs[1])
	move_leg(100,-30,z + 10,legs[2])
	time.sleep(breaklength)
	# position 8 put legs 5 and 6 down
	move_leg(100,30,z,legs[4])	
	move_leg(100,-30,z,legs[5])
	time.sleep(breaklength)
	#position 9 put legs 2 and 3 down and move them closer to the center than before
	time.sleep(breaklength)
	move_leg(100,30,z,legs[1])
	move_leg(100,-30,z,legs[2])
	time.sleep(breaklength)
#Before we  enter this function the current position is 

def moving_center(asterix,x,y,z,l=63.7):
	move_leg(100-x,y,z,legs[0])
	move_leg(100+x,-y,z,legs[3])
	move_leg(100+y,30+x,z,legs[4])
	move_leg(100+y,-30+x,z,legs[5])
	move_leg(100-y,30-x,z,legs[1])
	move_leg(100-y,-30-x,z,legs[2])
	time.sleep(0.2)

def rotation(asterix,y,y25,z):
	#clockwise 2 and 5 are limited
	breaklength = 0.5
	#position1
	moving_center(asterix,0,0,z,legs)
	#position2	put lags 2, 4, 6 in the air
	move_leg(100,30,z+20,legs[1])	
	move_leg(100,0,z+20,legs[3])
	move_leg(100,-30,z+20,legs[5])
	time.sleep(breaklength)
	#position3 rotate legs 2, 4, 6
	move_leg(100,30+y,z,legs[1])
	move_leg(100,y,z,legs[3])
	move_leg(100,-30+y,z,legs[5])
	time.sleep(breaklength)
	#position4 rotate legs 1, 3, 5
	move_leg(100,-30,z+20,legs[2])	
	move_leg(100,0,z+20,legs[0])
	move_leg(100,30,z+20,legs[4])
	time.sleep(breaklength)
	move_leg(100,-30+y,z,legs[2])	
	move_leg(100,y,z,legs[0])
	move_leg(100,30+y,z,legs[4])
	time.sleep(breaklength)	

def fast_rotation(asterix,y,z):
	breaklength = 1
	moving_center(asterix,0,0,z,legs)
	move_leg(100,-30,z+20,legs[5])
	move_leg(100,-30,z+20,legs[2])
	time.sleep(breaklength)	
	move_leg(100,0,z+20,legs[0])	
	move_leg(100,0,z+20,legs[3])
	time.sleep(breaklength)
	move_leg(100,y,z,legs[0])
	move_leg(100,y,z,legs[3])
	time.sleep(breaklength)
	move_leg(100,30,z+20,legs[1])
	move_leg(100,30,z+20,legs[4])
	time.sleep(breaklength)	
	move_leg(100,30+y,z,legs[1])
	move_leg(100,30+y,z,legs[4])
	time.sleep(breaklength)

def first_walk(asterix,x,y,z, legs, l=63.7):
	a=1

def walk_first_way():
	i = 0
	while 1:
		#position 1
		move_leg(150,0,-60,legs[0])
		move_leg(150,0,-60,legs[3])
		move_leg(100,30,-60,legs[5])
		move_leg(100,-30,-60,legs[4])
		move_leg(100,30,-60,legs[2])
		move_leg(100,-30,-60,legs[1])
		print "position 1"
		time.sleep(0.2)
		# position 2
		move_leg(100,-30,-30,legs[0])
		move_leg(100,30,-30,legs[3])
		print "position 2"
		time.sleep(0.2)
		# position 3
		move_leg(70,30,-60,legs[5])
		move_leg(70,-30,-60,legs[4])
		move_leg(130,30,-60,legs[2])
		move_leg(130,-30,-60,legs[1])
		print "position 3"
		time.sleep(0.2)
		# position 4
		move_leg(100,-30,-70,legs[0])
		move_leg(100,30,-70,legs[3])
		print "position 4"
		time.sleep(0.2)
		#position 5
		move_leg(100,30,-60,legs[5])
		move_leg(100,-30,-60,legs[4])
		move_leg(100,30,-60,legs[2])
		move_leg(100,-30,-60,legs[1])
		#print "position 5"
		time.sleep(0.2)
		i +=1
		print i

def walk_second_way(asterix,x,y,z, legs, l=63.7):
	# initial position (1)
	move_leg(100,0,-50,legs[0])
	move_leg(100,0,-50,legs[3])
	move_leg(100,120,-50,legs[5])
	move_leg(100,-120,-50,legs[4])
	move_leg(100,120,-50,legs[2])
	move_leg(100,-120,-50,legs[1])
	print "position 1"
	time.sleep(1)

	#position 2 : three legs ups, three on the ground
	move_leg(150,0,-20,legs[0])
	move_leg(100,120,-20,legs[2])
	move_leg(100,-120,-20,legs[4])
	print "position 2"
	time.sleep(1)

	#position 3
	while 1:
		move_leg(100,0,-70,legs[3])
		move_leg(50,-100,-70,legs[1])
		move_leg(50,100,-70,legs[5])
		time.sleep(1)

		#position 4
		move_leg(100,0,-90,legs[3])
		move_leg(50,-130,-70,legs[1])
		move_leg(50,130,-70,legs[5])
		time.sleep(1)

		#position 5
		move_leg(100,0,-90,legs[3])
		move_leg(50,-130,-70,legs[1])
		move_leg(50,130,-70,legs[5])
		time.sleep(1)

def walk_straight(asterix,x,y,z, legs, l=63.7):
	move_leg(150,0,0,legs[0])
	move_leg(150,0,0,legs[3])
	move_leg(100,30,-60,legs[5])
	move_leg(100,-30,-60,legs[4])
	move_leg(100,30,-60,legs[2])
	move_leg(100,-30,-60,legs[1])
	time.sleep(3)
	while 1:
		move_leg(100,-30,-50,legs[0])
		move_leg(100,30,-50,legs[3])
		move_leg(70,30,-60,legs[5])
		move_leg(70,-30,-60,legs[4])
		move_leg(130,30,-60,legs[2])
		move_leg(130,-30,-60,legs[1])
		time.sleep(0.5)

		move_leg(100,30,-50,legs[0])
		move_leg(100,-30,-50,legs[3])
		move_leg(130,30,-60,legs[5])
		move_leg(130,-30,-60,legs[4])
		move_leg(70,30,-60,legs[2])
		move_leg(70,-30,-60,legs[1])
		time.sleep(0.5)	


if __name__ == '__main__':
	# detection()
	asterix = initialize()
	# experimentation(obj)
	# motion(obj)
	legs = get_legs(asterix)
	while 1:
		rotation(asterix,100,50,-60)
	#moving_all_legs(asterix,100,30,-110,legs)
	# time.sleep(1)
	# for m in obj.motors:
		# m.goal_position = 0
		# time.sleep(0.5)
	# time.sleep(1)
	# walk_first_way(asterix,40,40,40,legs)
	# moving_center(asterix,0,-40,-60,legs)
	# moving_center(asterix,0,0,-60,legs)
	# moving_center(asterix,0,40,-60,legs)
	# moving_center(asterix,0,0,-60,legs)
	# while 1:
	# 	romantic_walk(asterix,30,0,-60)
	# moving_center(obj,40,30,-90)
		#moving_center(obj,0,-30,-90)
	# move_leg(150,0,-60,legs[0])
	# move_leg(150,0,-60,legs[3])
	# move_leg(100,100,-60,legs[5])
	# move_leg(100,-100,-60,legs[4])
	# move_leg(100,100,-60,legs[2])
	# move_leg(100,-100,-60,legs[1])

	asterix.close()

