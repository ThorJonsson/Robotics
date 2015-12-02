import itertools
import time
import numpy
import pypot.dynamixel

# we first open the Dynamixel serial port
with pypot.dynamixel.DxlIO('/dev/ttyUSB0', baudrate=1000000) as dxl_io:
    
    # we can scan the motors
    found_ids = dxl_io.scan() # this may take several seconds
    print 'original ids:', found_ids

    # we power on the motors
    dxl_io.enable_torque(found_ids)

    pos = dict(zip(found_ids, itertools.repeat(0)))
    dxl_io.set_goal_position(pos)
    time.sleep(1)
     
    leg1 = [11, 12, 13]
    leg2 = [21, 22, 23]
    leg3 = [31, 32, 33]
    leg4 = [41, 42, 43]
    leg5 = [51, 52, 53]
    leg6 = [61, 62, 63]
    
    pos = [0,0,30]
    
    #we change ids to ACW
    #change leg 2 to leg 8
    dxl_io.change_id({21 : 81, 22 : 82, 23 : 83})
    #change leg 3 to leg 7
    dxl_io.change_id({31 : 71, 32 : 72, 33 : 73})
    #change leg 5 to leg 3
    dxl_io.change_id({51 : 31, 52 : 32, 53 : 33})
    #change leg 6 to leg 2
    dxl_io.change_id({61 : 21, 62 : 22, 63 : 23})
    #change leg 7 to leg 5
    dxl_io.change_id({71 : 51, 72 : 52, 73 : 53})
    #change leg 8 to leg 6
    dxl_io.change_id({81 : 61, 82 : 62, 83 : 63})

    # we can scan new ids the motors
    found_ids = dxl_io.scan() # this may take several seconds
    print 'new ids:', found_ids
    

    pos = dict(zip(found_ids, itertools.repeat(0)))
    dxl_io.set_goal_position(pos)
    time.sleep(1)
    
    leg1 = [11, 12, 13]
    leg2 = [21, 22, 23]
    leg3 = [31, 32, 33]
    leg4 = [41, 42, 43]
    leg5 = [51, 52, 53]
    leg6 = [61, 62, 63]
    
    pos = [0,0,30]
    
    
    # we power off the motors
    #dxl_io.disable_torque(found_ids)
    time.sleep(1) # we wait for 1s
