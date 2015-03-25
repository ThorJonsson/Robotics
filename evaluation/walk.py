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
	
    angles = (0,0,0)
    theta1 = angles[0]
    theta2 = angles[1]
    theta3 = angles[2]

    try:
        theta1 = math.degrees(math.atan2(y3,x3))   # OK
        theta2 = math.degrees(math.atan(a1) + math.acos(tmp))
        theta3 = 180 - math.degrees(math.acos(a2))
        # Corrections to the angles theta2 and theta3
        theta2 = -(theta2 + alpha)
        theta3 = -(theta3 - 90 + alpha + beta)
        angles = (theta1,theta2,theta3)
    except ValueError:
        print "The legs of the robot cannot go that far!!"
        
    return angles

"""
Get the legs of the given robot object (from the json file).
"""
def get_legs(obj):
	return [obj.leg1,obj.leg2,obj.leg3,obj.leg4,obj.leg5,obj.leg6]

def move_leg(x,y,z,leg):
	
	i=0
	# tupl is a vector that carries the angles that represent the final position of the tip of the leg
	# the angles are calculated from the arguments of the function using inverse kinematics
	tupl = leg_ik(x,y,z)
	for m in leg.joints:
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
