# -*- coding: utf8 -*-

import math

"""
authors : Clément Renazeau, Thorsteinn Hjortur Jonsson , Corentin Charles
"""
def leg_dk(theta1,theta2,theta3,alpha,beta,l1=51,l2=63.7,l3=93):
	"""
	the next formula are used in the theorical case...
	"""
	
	# Convert angles to radians
	theta1 = math.radians(theta1)
	theta2 = math.radians(theta2)
	theta3 = math.radians(theta3)
	alpha = math.radians(alpha)
	beta = math.radians(beta)
	# Angles in degrees or radians ??
	coo = (None,None,None)
	x = (l1 + l2*math.cos(theta2 - alpha) + l3*math.cos(theta2 + theta3 - alpha + 90 - beta)) * math.cos(theta1)
	y = (l1 + l2*math.cos(theta2) + l3 * math.cos(theta2 + theta3)) * math.sin(theta1)
	z = l2 * math.sin(theta2 - alpha) + l3*math.sin(theta2 + theta3 - 90 + beta)
	
	coo = (x,y,z)
	
	return coo

print leg_dk(0,0,0,20.69,5.06)
