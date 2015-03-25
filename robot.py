import itertools
import time
import numpy
from pypot.dynamixel import autodetect_robot
import pypot.dynamixel
import math
import json
import time
from contextlib import closing
import Tkinter as tk

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

def move_leg(x,y,z,leg):
	
	i=0
	# tupl is a vector that carries the angles that represent the final position of the tip of the leg
	# the angles are calculated from the arguments of the function using inverse kinematics
	tupl = leg_ik(x,y,z)
	for m in leg:
		m.goal_position = tupl[i]
		i+=1

def moving_all_legs(asterix,x,y,z,legs):
	tupl = leg_ik(x,y,z)
	move_leg(x,y,z,legs[0])
	move_leg(x,y,z,legs[2])
	move_leg(x,y,z,legs[1])
	move_leg(x,y,z,legs[3])
	move_leg(x,y,z,legs[5])
	move_leg(x,y,z,legs[4])
# Before the center is in (0,0,-60)

"""
TODO: Currently the function is not using all the parameters. What happens when we replace current arguments to move_leg?
We need to be able to use arbitrary values. Au moins we need to be able to answer why we have choosen the current values
"""
def romantic_walk(asterix,x,y,z):
	breaklength = 0.2
	z = -60
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

"""
	Moving the center of the robot without changing the position of the tip of the legs.
TODO: What is the best value to use in order to obtain this action; Is it 100? does it make any more sense to use other parameters?
"""
def moving_center(asterix,x,y,z,l=63.7):
	# Experiments have shown that using the values 100 and 30 for changing x and y respectively is working okay
	move_leg(100-x,y,z,legs[0])
	move_leg(100+x,-y,z,legs[3])
	move_leg(100+y,30+x,z,legs[4])
	move_leg(100+y,-30+x,z,legs[5])
	move_leg(100-y,30-x,z,legs[1])
	move_leg(100-y,-30-x,z,legs[2])
	time.sleep(0.2)

def walk_gait(asterix):
	

"""--------------------- Rotation Functions ---------------------------"""
""" Written by Thor the 24/03/15 """
""" Tested by Corentin the 24/03/15 """
# This function takes care of 1 leg at a time
# This moves the leg given polar coordinates. Important because we when we need to do a rotation the legs should not move
# outside the circle of rotation. We want a perfect rotation!
# TEST : Working perfectly
def move_leg(theta,z,leg,R = 100):
	
	i=0
	# Tupl is a vector that carries the angles that represent the final position of the tip of the leg
	# The angles are calculated from the arguments of the function using inverse kinematics
	# R is the radius of the circle of rotation. Theta is given in degrees. 
	# Lets transform our polar coordinates onto the Cartesian plane
	x = R*math.cos(math.radians(theta))
	y = R*math.sin(math.radians(theta))
	motor_angles = leg_ik(x,y,z)
	for m in leg:
		m.goal_position = motor_angles[i]
		i+=1

# This should just give us our initial spider position
# We also use this function when rotating to refix the legs' frames of reference
"""SOLVED?"""
#TEST : We SHOULD NOT put negative value in this function (otehrwise the legs (except legs 1-4) will 'meet each other')
def initial_pos(asterix,theta,z):
	# Experiments have shown that using the values 100 and 30 for changing x and y respectively is working okay
	move_leg(0,z,legs[0])
	move_leg(abs(theta),z,legs[1])
	move_leg(-abs(theta),z,legs[2])
	move_leg(0,z,legs[3])
	move_leg(abs(theta),z,legs[4])
	move_leg(-abs(theta),z,legs[5])

	time.sleep(0.1)

"""
TODO: make sure that this works. If it works than we can easily do experiments to find the highest value on alpha
If we know the highest value of alpha we can determine the number of turns needed to do an arbitrary amount of rotation by using Euclidean division
See the draft implementation for arbitrary_rotation above.
"""
# theta is the value we need to set the initial position
# alpha determines the amount of rotation (made by each call to the function) from this initial position
# alpha is physically limited because of the legs. We should define this limit as max_angle - see above.
# TEST : A value of 45 will make the legs (2-3 and 4-5) touch for a little while (actually until the next leg move)
def rotation_angle(asterix,alpha,theta,z):
	#clockwise 2 and 5 are limited
	breaklength = 0.1
	# Position 1: The 'spider' position. This position has a low center of gravity. 
	# Here we define the initial position. i.e. the spider position
	# It is important to observe the x and y values of each leg in its own frame of reference
	
	# Position 2: Put legs 1, 3, 5 in the air and rotate at the same time
	move_leg(theta+alpha,z+20,legs[1])	
	move_leg(alpha,z+20,legs[3])
	move_leg(-theta+alpha,z+20,legs[5])
	time.sleep(breaklength)

	# Position 3: Put legs 1,3 and 5 down
	move_leg(theta+alpha,z,legs[1])	
	move_leg(alpha,z,legs[3])
	move_leg(-theta+alpha,z,legs[5])
	time.sleep(breaklength)
	
	# Position 4: Rotate legs 0, 2, 4
	move_leg(alpha,z+20,legs[0])
	move_leg(-theta+alpha,z+20,legs[2])	
	move_leg(theta+alpha,z+20,legs[4])
	time.sleep(breaklength)

	# Position 5: Put legs 0, 2 and 4 down.
	move_leg(alpha,z,legs[0])
	move_leg(-theta+alpha,z,legs[2])	
	move_leg(theta+alpha,z,legs[4])
	time.sleep(breaklength)

# max_angle = 20 is just a guess. 
# TEST : Working not too bad. beta = 180 are doing a rotation of 90deg. It seems that we have to multiply the wanted value by 2 to have a proper rotation
"""SOLVED?""" 
#TEST : If we put negative value fot the beta angle, this is just not working.
# TEST : If the value of max_angle is not 20, the rotation does not work proprely
# theta and z are simply values that determine the initial position
# Other parameters are to define the rotation
def arbitrary_rotation(asterix,beta, max_angle = 20, theta = 15, z = -60):
# Here we do euclidean division. We determine how often max_angle divides beta and the remainder of this division.
# This gives us the number of rotations we need to make by a predefined max_angle 
# The remainder gives us the amount we need to rotate by to be able to finish the full rotation by an angle of beta
# i.e. beta = q*max_angle + r
	initial_pos(asterix,theta,z)
	if beta < 0:
		max_angle = -max_angle

	q = beta//max_angle 
	r = beta%max_angle

	# rotate by max_angle q times
	for i in range(1,q):
		rotation_angle(asterix,max_angle, theta, z)
		initial_pos(asterix,theta,z)
	# finally rotate by r 
	rotation_angle(asterix,r, theta, z)
	initial_pos(asterix,theta,z)


""" ----------------------------------------------------------------------- """

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
	time.sleep(2)
	# asterix = pypot.robot.from_json('my_robot.json')

	# experimentation(obj)
	# motion(obj)
	legs = get_legs(asterix)
	
	arbitrary_rotation(asterix,360)






	# walk_first_way()


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

