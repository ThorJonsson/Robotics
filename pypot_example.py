import itertools
import time
import numpy
import pypot.dynamixel

# Before: We assume we've not scanned the motors as we'd like to run this     # function only at the beginning of each session. Therefore it makes no sense # to not include it in this function.
# After: We've scanned the motors and renamed them 
def change_motorid():
    # We can scan the motors
    found_ids = dxl_io.scan()#   this may take several seconds
    # It is essential to know the current labels to prevent from making errors
    print 'Detected:', found_ids
    
    # This loop goes through all the motors and asks the user to relabel
    for motor_id in found_ids:
        print "When labelling the motors please do not use any of the already detected ones as it will produce an error!"
        # Lights up the motor 
        dxl_io.switch_led_on(motor_id)
        # I think it is only possible to use integers but I can't find any    # documentation
        new_id = int(input("Please enter an integer to label the lit motor"))
        dxl_io.change_id({motor_id : new_id})
    # To check whether everything went according to plan    
    found_ids = dxl_io.scan()
    print "The new id's are: ", found_ids
  
  
if __name__ == '__main__':

    # we first open the Dynamixel serial port
    with pypot.dynamixel.DxlIO('/dev/ttyUSB0', baudrate=1000000) as dxl_io:    
        change_motorid(found_ids)
        # we power on the motors
        dxl_io.enable_torque(found_ids)
        # we get the current positions
        print 'Current pos:', dxl_io.get_present_position(found_ids)
        # Saves the current time	
        T0 = time.time()
        # We let this variable run with the loop
        T = T0
        freq = 2
        # We make the loop run for 10 seconds
        # This loop makes the actuators move with a sinusoidal frequency.
        while T < T0 + 10:

            # we create a python dictionnary: {id0 : position0, id1 : position1...}
            # pos should be equal to:
            # {found_ids[0] : 10*numpy.sin(numpy.pi*2*freq*T), found_ids[1] : 10*numpy.sin(numpy.pi*2*freq*T), found_ids[2] : 10*numpy.sin(numpy.pi*2*freq*T)}
            # This sets the position
            pos = dict(zip(found_ids, 10*numpy.sin(numpy.pi*2*freq*T))
            #print 'Cmd:', pos
            T = time.time()
            # This moves it to the set position
            dxl_io.set_goal_position(pos)
            # It is unreasonable to make the actuator move more often than 50 # times per second.
            time.sleep(0.02)  # we wait for 0.02s
        
        
        

        # we get the current positions
        print 'New pos:', dxl_io.get_present_position(found_ids)
        # we power off the motors
        dxl_io.disable_torque(found_ids)
        time.sleep(1)  # we wait for 1s
