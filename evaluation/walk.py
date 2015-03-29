import time #used for the sleep function
from pypot.dynamixel import autodetect_robot	#used to get the robot object
import pypot.dynamixel	#used to get the motors,legs etc.
import math #quite obvious
import json	#to use a json file
from contextlib import closing	#to close properly the robot at  the end
import pypot.robot
import rotation

import Tkinter as tk # to get the a graphic interface for the control function


asterix = None
legs = []
initial = []

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

"""
	Makes one leg move.
	parameters:
		L -- The length between the start point and the end point (in a right line)
		leg -- The leg we want to move
		initial -- a tuple with three values wich correspond to the intial coordonnate of the end of the leg
"""
def move_leg(L,z,leg):
	num = int(leg[0].id*0.1)-1
	theta = math.atan(initial[num][1]/initial[num][0])
	hypo = math.sqrt(initial[num][0]**2 + initial[num][1]**2)
	x = math.cos(theta)*(hypo+L)
	y = math.sin(theta)*(hypo+L)
	z = z
	angles = leg_ik(x,y,z)
	i=0
	for motors in leg:
		motors.goal_position = angles[i]
		i+=1
""""
Make the robot move along his two separate legs
"""
def move_center_forward(L,z):
	break_length = 1
	theta = 20	#more than 20 would make the legs touch for a sec (because of the speed)
	order = [1,5,2,4]
	if L<0:
		order = [4,2,5,1]

	move_leg(L,z+40,legs[0])
	move_leg(-L,z+40,legs[3])
	time.sleep(break_length)

	move_leg(L,z,legs[0])
	move_leg(-L,z,legs[3])
	time.sleep(break_length)
	for i in order:
		if i==order[0] or i==order[2]:
			rotation.move_leg(-theta,z+40,legs[i])
		else:
			rotation.move_leg(theta,z+40,legs[i])
			time.sleep(break_length)
	for i in order:
		if i==order[0] or i==order[2]:
			rotation.move_leg(-theta,z,legs[i])
		else:
			rotation.move_leg(theta,z,legs[i])
			time.sleep(break_length)
	time.sleep(break_length)

"""
THEORICAL WORK: The order of the leg or the direction could be wrong...TO TEST
Make the robot move along its two legged side.
"""
def move_center_aside(L,z):

	break_length = 1
	theta = 20
	if L<0:
		theta = -theta

	initial = rotation.initial_pos(0,-60)
	time.sleep(break_length)
	move_leg(L,z+40,legs[1])
	move_leg(L,z+40,legs[2])
	time.sleep(break_length)
	move_leg(L,z,legs[1])
	move_leg(L,z,legs[2])
		
	
	move_leg(-L,z+40,legs[4])
	move_leg(-L,z+40,legs[5])
	time.sleep(break_length)
	move_leg(-L,z,legs[4])
	move_leg(-L,z,legs[5])
	time.sleep(break_length)

	rotation.move_leg(theta,z+40,legs[0])
	rotation.move_leg(theta,z+40,legs[3])
	time.sleep(break_length)
	rotation.move_leg(theta,z,legs[0])
	rotation.move_leg(theta,z,legs[3])
	time.sleep(break_length)

def moving_all_legs(L,z):
	move_leg(L,z,legs[0])
	move_leg(L,z,legs[1])
	move_leg(L,z,legs[2])
	move_leg(-L,z,legs[3])
	move_leg(L,z,legs[4])
	move_leg(L,z,legs[5])
