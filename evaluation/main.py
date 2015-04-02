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
from Tkinter import *
import functools
import pypot.robot

asterix = None
legs = []



def get_object():
	"""
		Return a robot object created from a json file. initialize the legs variable in the three files.
	"""
	asterix = pypot.robot.from_json('my_robot.json')
	legs = get_legs(asterix)
	rotation.legs = get_legs(asterix)
	walk.legs = get_legs(asterix)

	return asterix


def detection():
	"""
		Do the detection of the robot with all its motors. It puts the configuration into a json file named 'my_robot.json'
	"""
	my_robot = autodetect_robot() #detect al the legs of the robot. Might take a while to operate.

	config = my_robot.to_config()
	with open('my_robot.json', 'wb') as f:
	    json.dump(config, f)

	with closing(pypot.robot.from_json('my_robot.json')) as my_robot:
	    # do stuff without having to make sure not to forget to close my_robot!
	    pass
 
  
def initialize():
	"""
		Initialize the robot. Firstly get the robot object, and then put the angles of the motor at 0 deg.
		Return the robot object.
	"""  
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


def get_legs(obj):
	"""
		Return a list with all the legs of the robot passed in parameter, i.e a leg is three motors. The motorgroups is actually done manually.
	"""
	return [obj.leg1,obj.leg2,obj.leg3,obj.leg4,obj.leg5,obj.leg6]

#--------------------------------------
#--------- Graphic interface ----------
#--------------------------------------

def create_interface():

	window = Tk()

	cadre = Frame(window, width=700, height=500, borderwidth=1)
	cadre.pack(fill=BOTH)

	#move forward
	forward = Frame(cadre, width=700, height=100, borderwidth=1)
	forward.pack(fill=Y)
	message = Label(forward, text="Move Forward")
	message.pack(side="left") 

	var_texte_1 = StringVar()
	ligne_texte = Entry(forward, textvariable=var_texte_1, width=5)
	ligne_texte.pack(side="left")

	message = Label(forward, text="mm")
	message.pack(side="left") 

	bouton_forward = Button(forward, text="Move Forward", fg="red",command=functools.partial(walk.move_center_forward,L=ligne_texte.get()))
	bouton_forward.pack(side="left") 

	#move aside
	aside = Frame(cadre, width=700, height=100, borderwidth=1)
	aside.pack(fill=Y)
	message = Label(aside, text="Move Aside")
	message.pack(side="left")

	var_texte_2 = StringVar()
	ligne_texte = Entry(aside, textvariable=var_texte_2, width=5)
	ligne_texte.pack(side="left")

	message = Label(aside, text="mm")
	message.pack(side="left")

	bouton_aside = Button(aside, text="Move Aside", fg="red",command=window.quit)
	bouton_aside.pack(side="left") 

	#rotation
	rotation = Frame(cadre, width=700, height=100, borderwidth=1)
	rotation.pack(fill=Y)
	message = Label(rotation, text="Rotation")
	message.pack(side="left")

	var_texte_3 = StringVar()
	ligne_texte = Entry(rotation, textvariable=var_texte_3, width=5)
	ligne_texte.pack(side="left")

	message = Label(rotation, text="degres")
	message.pack(side="left")

	bouton_aside = Button(rotation, text="Rotation", fg="red",command=window.quit)
	bouton_aside.pack(side="left") 

	window.mainloop()
	window.destroy()


if __name__ == '__main__':
    
	# asterix = get_object()
	initialize()
	walk.initial = rotation.initial_pos(30,-60)
	time.sleep(0.1)
	create_interface()
	while 1:
		walk.move_center_forward(20,-60)
		walk.initial = rotation.initial_pos(30,-60)
	# We really need to sleep before we die
	# rotation.arbitrary_rotation(360)	
	time.sleep(0.1)

	
