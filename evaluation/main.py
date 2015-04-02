import walk as walk
import rotation as rotation

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


"""
	Return a robot object created from a json file. initialize the legs variable in the three files.
"""
def get_object():
	asterix = pypot.robot.from_json('my_robot.json')
	legs = get_legs(asterix)
	rotation.legs = get_legs(asterix)
	walk.legs = get_legs(asterix)

	return asterix

"""
	Do the detection of the robot with all its motors. It puts the configuration into a json file named 'my_robot.json'
"""
def detection():

	my_robot = autodetect_robot() #detect al the legs of the robot. Might take a while to operate.

	#write the configuration found into a json file. We shouldn't use the complete detection whith this json file.
	config = my_robot.to_config()
	with open('my_robot.json', 'wb') as f:
	    json.dump(config, f)

	with closing(pypot.robot.from_json('my_robot.json')) as my_robot:
	    # do stuff without having to make sure not to forget to close my_robot!
	    pass
 
"""
	Initialize the robot. Firstly get the robot object, and then put the angles of the motor at 0°.
	Return the robot object.
"""    
def initialize():

	asterix = get_object()
	# print asterix
	# Note that all these calls will return immediately,
	# and the orders will not be directly sent
	# (they will be sent during the next write loop iteration).
	for m in asterix.motors:
	    m.compliant = False		# <=> enable_torque.
	   # m.goal_position = 0
	time.sleep(0.1)
	return asterix
"""
	if asterix['motorgroups'] == None:
		asterix['motorgroups'] = {
		'leg1': ["motor_11","motor_12","motor_13"],
		'leg2': ["motor_21","motor_22","motor_23"],
		'leg3': ["motor_31","motor_32","motor_33"],
		'leg4': ["motor_41","motor_42","motor_43"],
		'leg5': ["motor_51","motor_52","motor_53"],
		'leg6': ["motor_61","motor_62","motor_63"]
		}
"""

"""
	Return a list with all the legs of the robot passed in parameter, i.e a leg is three motors. The motorgroups is actually done manually.
"""
def get_legs(obj):
    return [obj.leg1,obj.leg2,obj.leg3,obj.leg4,obj.leg5,obj.leg6]


#----------------------------------------------
#--------------- events function --------------
#----------------------------------------------

"""
	Call the move_center_forward function with some defined values.
	Parameters : 
		-- event : an event that 'catch' what key the users is pressing.
"""
def forward(event):
     z = -60
     L = 30
     theta = 0
     break_length = 0.2
     walk.initial = rotation.initial_pos(theta,z)
     time.sleep(break_length)
     walk.move_center_forward(L,z)
     walk.initial = rotation.initial_pos(theta,z)
     time.sleep(break_length)

"""
	Call the move_center_forward function with some defined valuees (one is negative to go be able to go backward).
	Parameters : 
		-- event : an event that 'catch' what key the users is pressing.
"""
def backward(event):
     z = -60
     L = -30
     theta = 0
     break_length = 0.2
     walk.initial = rotation.initial_pos(theta,z)
     time.sleep(break_length)
     walk.move_center_forward(L,z)
     walk.initial = rotation.initial_pos(theta,z)
     time.sleep(break_length)

"""
	Call the move_center_aside function with some defined values.
	Parameters : 
		-- event : an event that 'catch' what key the users is pressing.
"""
def left(event):
     z= -60
     L = 30
     theta = 0
     break_length = 0.2
     walk.move_center_aside(L,z)

"""
	Call the move_center_aside function with some defined values.
	Parameters : 
		-- event : an event that 'catch' what key the users is pressing.
"""
def right(event):
     z= -60
     L = -30
     theta = 0
     break_length = 0.2
     walk.move_center_aside(L,z)

"""
	Call the arbitrary_rotation function with some defined values.
	Parameters : 
		-- event : an event that 'catch' what key the users is pressing.
"""
def rotation_left(event):
     angle = 90
     rotation.arbitrary_rotation(angle*2)

"""
	Call the arbitrary_rotation function with some defined values (one is negative).
	Parameters : 
		-- event : an event that 'catch' what key the users is pressing.
"""
def rotation_right(event):
     angle = -90
     rotation.arbitrary_rotation(angle*2)

"""
	Call the initial_pos function with some defined values, with a height of 60 cm.
	Parameters : 
		-- event : an event that 'catch' what key the users is pressing.
"""
def position_intial(event):
     theta = 0
     z = -60
     rotation.initial_pos(theta,z)

"""
	Bind all the events to the minimal graphinc interface.
"""
def user_interaction():
     root = Tk()
     root.bind("<Up>",forward)
     root.bind("<Down>",backward)
     root.bind("<Right>",right)
     root.bind("<Left>",left)
     root.bind("<i>",rotation_left)
     root.bind("<i>",rotation_right)
     root.bind("<Return>",position_initial)
     root.mainloop()


if __name__ == '__main__':
    
	# asterix = get_object()
	initialize()
	walk.initial = rotation.initial_pos(30,-60)
	#while 1:
	#	walk.move_center_aside(10,-60)
	# We really need to sleep before we die
	rotation.arbitrary_rotation(360)	
	time.sleep(0.1)

	
