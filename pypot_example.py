import itertools
import time
import numpy
import pypot.dynamixel

def change_motorid(found_ids):
    for i in [0,1,2]:
	dxl_io.change_id({found_ids[i] : 10+i})
  
  
if __name__ == '__main__':

    # we first open the Dynamixel serial port
    with pypot.dynamixel.DxlIO('/dev/ttyUSB0', baudrate=1000000) as dxl_io:

        # we can scan the motors
        found_ids = dxl_io.scan()#   this may take several seconds
        #change_motorid(found_ids)
        print 'Detected:', found_ids
        
	change_motorid(found_ids)
	found_ids = dxl_io.scan()
	print 'Detected:', found_ids
        # we power on the motors
        dxl_io.enable_torque(found_ids)

        # we get the current positions
        print 'Current pos:', dxl_io.get_present_position(found_ids)
	T0 = time.time()
	T = T0
	freq = 2
	""""while T < T0 + 10:
	
	# we create a python dictionnary: {id0 : position0, id1 : position1...}
	  pos = {found_ids[0] : 10*numpy.sin(numpy.pi*2*freq*T), found_ids[1] : 10*numpy.sin(numpy.pi*2*freq*T), found_ids[2] : 20*numpy.sin(numpy.pi*2*freq*T)}#dict(zip(found_ids, itertools.repeat(0)))
	  #print 'Cmd:', pos
	  T = time.time()
	  dxl_io.set_goal_position(pos)
	  time.sleep(0.02)  # we wait for 1s
        # we send these new positions
        """
        

        # we get the current positions
        print 'New pos:', dxl_io.get_present_position(found_ids)

        # we power off the motors
        dxl_io.disable_torque(found_ids)
        time.sleep(1)  # we wait for 1s
