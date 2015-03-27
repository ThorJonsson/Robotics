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

def get_legs(obj):
    return [obj.leg1,obj.leg2,obj.leg3,obj.leg4,obj.leg5,obj.leg6]

if __name__ == '__main__':
    
	asterix = initialize()
	rotation.legs = get_legs(asterix)

	walk.legs = get_legs(asterix)
	walk.initial = rotation.initial_pos(asterix,0,-80)
	print "walk.initial() : ",walk.initial
	time.sleep(2)
	walk.move_leg(30,walk.legs[0])
	time.sleep(0.2)
    # print rotation.legs[0][0].id
	# rotation.move_leg(0,-60,rotation.legs[0])
	# rotation.arbitrary_rotation(asterix,720)