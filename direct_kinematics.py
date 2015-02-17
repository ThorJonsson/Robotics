# -*- coding: utf8 -*-

import math

def leg_dk(theta1,theta2,theta3,alpha,beta,l1=51,l2=63.7,l3=93):
	"""
	the next formula are used in the theorical case...
	"""
	# Angles in degrees or radians ??
	coo = (None,None,None)
	x = (l2 + l2*math.cos(theta2 + alpha) + l3*math.cos(theta2 + theta3 + 90 - beta)) * math.cos(theta1)
	y = (l1 + l2 * math.cos(theta2 + theta3)) * math.sin(theta1)
	z = l2 * math.sin(theta2 + alpha) + l3*math.sin(theta2 + theta3 + 90 - beta)
	
	coo = (x,y,z)
	
	return coo

