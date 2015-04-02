import time #used for the sleep function
from pypot.dynamixel import autodetect_robot	#used to get the robot object
import pypot.dynamixel	#used to get the motors,legs etc.
import math #quite obvious
import json	#to use a json file
from contextlib import closing	#to close properly the robot at  the end
import pypot.robot

legs = []
xCorrection = [-10,-20,-20,10,-20,-20]
yCorrection = [0,-15,15,0,15,-15]


"""
	Indirect kinematic function.
	Parameters : 
		- (x3,y3,z3) : The coordonnates where we want to put the leg
		- alpha : the correction for the second motor.
		- beta : the correction for the third motor.
		- l2, l3 : the length of the different part of the leg
	Return a tuple with three values, corresponding to the angles of each motor of the leg.
"""
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
        print "The leg of the robot cannot go that far!!"
        
    return angles


def get_legs(obj):
    """
	Return a list with all the legs of the robot passed in parameter, i.e a leg is three motors. The motorgroups is actually done manually.
	"""
    return [obj.leg1,obj.leg2,obj.leg3,obj.leg4,obj.leg5,obj.leg6]


def get_xCorrection(leg):
	"""
		Return the correction (in mm) for the x axis of a specified leg
		Parameters : 
			- leg : The leg which is going to be moved
	"""
	i = int(leg[0].id*0.1)
	return xCorrection[i-1]


def get_yCorrection(leg):
	"""
	Return the correction (in mm) for the y axis of a specified leg
	Parameters : 
		- leg : The leg which is going to be moved
	"""
	i = int(leg[0].id*0.1)
	return yCorrection[i-1]

def R_leg(theta,leg,R_center):
	"""
		

	"""
	xCorrection = get_xCorrection(leg)
	yCorrection = get_yCorrection(leg)
	cos = math.cos(math.radians(theta))
	sin = math.sin(math.radians(theta))
	tmp = (xCorrection**2)*((cos**2)-1)
	tmp += (yCorrection**2)*((sin**2)-1)
	tmp += xCorrection*yCorrection*math.sin(2*math.radians(theta))
	tmp += R_center**2
	return (-xCorrection*cos - yCorrection*sin + math.sqrt(tmp))

def move_leg(theta,z,leg,R_center = 100):
	"""
		Do a rotation on one leg.
		Parameters : 
			- theta : the angle we want the leg to do
			- z : the height of the tip of the leg.
			- leg : the leg we want to move
			- R_center : The radius of the circle which the center is equal to center of the entire robot. 
		Return a tuple with the coordonnates of the leg.
	"""
	i=0
	# Tupl is a vector that carries the angles that represent the final position of the tip of the leg
	# The angles are calculated from the arguments of the function using inverse kinematics
	# R is the radius of the circle of rotation. Theta is given in degrees. 
	# Lets transform our polar coordinates onto the Cartesian plane
	# print R_leg(theta,leg,R), " - ", leg[0].id
	x = R_leg(theta,leg,R_center)*math.cos(math.radians(theta))
	y = R_leg(theta,leg,R_center)*math.sin(math.radians(theta))
	motor_angles = leg_ik(x,y,z)
	for m in leg:
		m.goal_position = motor_angles[i]
		i+=1
	return (x,y,z)

def initial_pos(theta,z):
	"""
		Put the robot in an initial position.
		Parameters :
			- theta : The initial angle of the leg from on its own axis.
			- z : The height of the leg.
	"""
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

def rotation_angle(alpha,theta,z):
	"""
		Do a rotation on all the legs of the robot.
		Parameters :
			- alpha : 
			- theta : The angle we want the legs to do.
			- z : the height of the leg.
	"""
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

def arbitrary_rotation(beta, max_angle = 10, theta = 45, z = -60):
	"""
		Do a fully operational rotation on the robot (the return to inital position is in this function)
		Parameters :
			- beta : The angle we want the center of the robot to do.
			- max_angle : The maximum angle the robot can do in one loop.
			- theta : The rotation of each leg.
			- z : the height of the robot.
	"""

	beta = 2*beta
	initial_pos(theta,z)
	if beta < 0:
		max_angle = -max_angle

	q = beta//max_angle 
	r = beta%max_angle
	print q
	print r
	# rotate by max_angle q times
	for i in range(1,q):
		rotation_angle(max_angle, theta, z)
		initial_pos(theta,z)
	# finally rotate by r 
	rotation_angle(r, theta, z)
	initial_pos(theta,z)

