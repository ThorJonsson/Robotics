import time #used for the sleep function
from pypot.dynamixel import autodetect_robot	#used to get the robot object
import pypot.dynamixel	#used to get the motors,legs etc.
import math #quite obvious
import json	#to use a json file
from contextlib import closing	#to close properly the robot at  the end
import pypot.robot

asterix = None
legs = []
xCorrection = [80,0,0,80,0,0]
yCorrection = [0,0,0,0,0,0]



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

def get_xCorrection(leg):
	i = int(leg[0].id*0.1)
	return xCorrection[i-1]

def get_yCorrection(leg):
	i = int(leg[0].id*0.1)
	return yCorrection[i-1]

"""--------------------- Rotation Functions ---------------------------"""
""" Written by Thor the 24/03/15 """
""" Tested by Corentin the 24/03/15 """


""" -------------------Mathematics to correct the rotation ------------"""
""" Written by Thor the 26/04/15"""
# This needs to be done so that we can define a common circle of rotation
# for all the legs. To communicate this common information to all the legs
# we need to express the radius of this common circle of rotation as a function of theta and the legs 
""" I added the attributes needed to obtain this information to the json file
Currently these attributes are set to zero"""
def R_leg(theta,leg,R):
	xCorrection = get_xCorrection(leg)
	yCorrection = get_yCorrection(leg)
	cos = math.cos(math.radians(theta))
	sin = math.sin(math.radians(theta))
	tmp = (xCorrection**2)*((cos**2)-1)
	tmp += (yCorrection**2)*((sin**2)-1)
	tmp += xCorrection*yCorrection*math.sin(math.radians(2*theta))
	tmp += R**2
	return (-xCorrection*cos - yCorrection*sin + math.sqrt(tmp))


# This function takes care of 1 leg at a time
# This moves the leg given polar coordinates. Important because we when we need to do a rotation the legs should not move
# outside the circle of rotation. We want a perfect rotation!
# TEST : Working perfectly
def move_leg(theta,z,leg,R = 150):
	
	i=0
	# Tupl is a vector that carries the angles that represent the final position of the tip of the leg
	# The angles are calculated from the arguments of the function using inverse kinematics
	# R is the radius of the circle of rotation. Theta is given in degrees. 
	# Lets transform our polar coordinates onto the Cartesian plane
	# print R_leg(theta,leg,R), " - ", leg[0].id
	x = R_leg(theta,leg,R)*math.cos(math.radians(theta))+get_xCorrection(leg)
	y = R_leg(theta,leg,R)*math.sin(math.radians(theta))+get_yCorrection(leg)
	motor_angles = leg_ik(x,y,z)
	for m in leg:
		m.goal_position = motor_angles[i]
		i+=1
	return (x,y)

# This should just give us our initial spider position
# We also use this function when rotating to refix the legs' frames of reference
"""SOLVED?"""
#TEST : We SHOULD NOT put negative value in this function (otehrwise the legs (except legs 1-4) will 'meet each other')
def initial_pos(asterix,theta,z):
	# Experiments have shown that using the values 100 and 30 for changing x and y respectively is working okay
	initial_position = []
	initial_position.append(move_leg(0,z,legs[0]))
	initial_position.append(move_leg(-abs(theta),z,legs[1]))
	initial_position.append(move_leg(abs(theta),z,legs[2]))
	initial_position.append(move_leg(0,z,legs[3]))
	initial_position.append(move_leg(-abs(theta),z,legs[4]))
	initial_position.append(move_leg(abs(theta),z,legs[5]))

	time.sleep(0.1)

	return initial_position

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
	move_leg(-abs(theta)+alpha,z+20,legs[1])	
	move_leg(alpha,z+20,legs[3])
	move_leg(abs(theta)+alpha,z+20,legs[5])
	time.sleep(breaklength)

	# Position 3: Put legs 1,3 and 5 down
	move_leg(-abs(theta)+alpha,z,legs[1])	
	move_leg(alpha,z,legs[3])
	move_leg(abs(theta)+alpha,z,legs[5])
	time.sleep(breaklength)
	
	# Position 4: Rotate legs 0, 2, 4
	move_leg(alpha,z+20,legs[0])
	move_leg(abs(theta)+alpha,z+20,legs[2])	
	move_leg(-abs(theta)+alpha,z+20,legs[4])
	time.sleep(breaklength)

	# Position 5: Put legs 0, 2 and 4 down.
	move_leg(alpha,z,legs[0])
	move_leg(abs(theta)+alpha,z,legs[2])	
	move_leg(-abs(theta)+alpha,z,legs[4])
	time.sleep(breaklength)

# max_angle = 20 is just a guess. 
# TEST : Working not too bad. beta = 180 are doing a rotation of 90deg. It seems that we have to multiply the wanted value by 2 to have a proper rotation
"""SOLVED?""" 
#TEST : If we put negative value fot the beta angle, this is just not working.
# TEST : If the value of max_angle is not 20, the rotation does not work proprely
# theta and z are simply values that determine the initial position
# Other parameters are to define the rotation
def arbitrary_rotation(asterix,beta, max_angle = 20, theta = 45, z = -60):
# Here we do euclidean division. We determine how often max_angle divides beta and the remainder of this division.
# This gives us the number of rotations we need to make by a predefined max_angle 
# The remainder gives us the amount we need to rotate by to be able to finish the full rotation by an angle of beta
# i.e. beta = q*max_angle + r
	initial_pos(asterix,theta,z)
	if beta < 0:
		max_angle = -max_angle

	q = beta//max_angle 
	r = beta%max_angle
	print q
	print r
	# rotate by max_angle q times
	for i in range(1,q):
		rotation_angle(asterix,max_angle, theta, z)
		initial_pos(asterix,theta,z)
	# finally rotate by r 
	rotation_angle(asterix,r, theta, z)
	initial_pos(asterix,theta,z)


""" ----------------------------------------------------------------------- """
