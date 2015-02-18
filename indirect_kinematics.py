# -*- coding: utf8 -*-

import math
tmp = None

def leg_dk(x3,y3,z3,alpha = 20.69, beta = 5.06,l1=51,l2=63.7,l3=93):
	
	d13 = math.sqrt(x3*x3 + y3*y3) - l1
	d = math.sqrt(d13*d13 + z3*z3)
	
	tmp = (l2*l2 + d*d - l3*l3)/(2*l2*d)
	a1 = z3 / d13
	a2 = (l2*l2 + l3*l3 - d*d)/(2*l2*l3)
	print a2
	print a1
	print tmp
	
	angles = (None,None,None)
	theta1 = math.degrees(math.atan2(y3,x3))
	theta2 = math.degrees(math.atan(a1) + math.acos(tmp))
	theta3 = 180 - math.degrees(math.acos(a2))
	# Corrections to the angles theta2 and theta3
	theta2 = theta2 + alpha
	theta3 = theta3 - 90 + alpha + beta
	angles = (theta1,theta2,theta3)
	
	return angles

#~ print leg_dk(118.79,0,-115.14)
#~ print leg_dk(0,118.79,-115.14)
#~ print leg_dk(-64.14,0,-67.79)
print leg_dk(203.23,0,-14.30)
