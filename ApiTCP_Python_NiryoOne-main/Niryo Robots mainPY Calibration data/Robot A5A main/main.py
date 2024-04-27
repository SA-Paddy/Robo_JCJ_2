
import time
from niryo_one_tcp_client import *
import keyboard

import os
# ROBOT A5A

x=0.219
y=-0.061
z=0.167
r=1.469
p=1.528
ya=-0.071
key=' '
incr=0.001 # increment value for all axes; May be changed to
           # different values for each axis
# ROBOT JOINT COORDINATES
J1=-0.251
J2=-0.496
J3=-0.552
J4=-0.049
J5=-0.502
J6=1.331
def main():

    global x,y,z,r,p,ya,incr

    print(" Niryo 1 Robot Control Program")

    # Connect to the Robot Wireless Hotspot
    n1 = NiryoOneClient()
    status = n1.connect("10.10.10.10")

    position_keys()

    n1.change_tool(RobotTool.GRIPPER_1)
    n1.open_gripper(RobotTool.GRIPPER_1, 1000)
    status, data = n1.calibrate(CalibrateMode.AUTO)

    # go to initial position defined above
    n1.move_joints(J1,J2,J3,J4,J5,J6)
    n1.move_pose(x, y, z, r, p, ya)
    # stay in the while loop below
    while True:


        if keyboard.read_key()=="x":
            x=x+incr
        elif keyboard.read_key()=="c":
            x=x-incr
        elif keyboard.read_key()=="y":
            y=y+incr
        elif keyboard.read_key()=="u":
            y=y-incr
        elif keyboard.read_key()=="z":
            z=z+incr
        elif keyboard.read_key()=="a":
            z=z-incr

        elif keyboard.read_key()=="-":
            n1.open_gripper(RobotTool.GRIPPER_1, 1000)
        elif keyboard.read_key()=="+":
            n1.close_gripper(RobotTool.GRIPPER_1, 1000)

        elif keyboard.read_key()=="q":

        # when 'q' is pressed , break out of the loop
             break
        #Clears the screen preventing it from being populated continuously with data
        clear_screen()
        # function that print Labels for position keys x,y,z axis
        position_keys()
        # --------------------------------------------------------
        print("----------------------------------------------------")
        print("       x        y       z  ")
        # print the pose /world coordinatesxxx
        print(key,"  ",round(x,7)," ",round(y,7)," ",round(z,7)," ",r," ",p," ",ya)

        #move the Robot
        n1.move_pose(x, y, z, r, p, ya)
# END of WHILE: remain in the while loop until 'q' is pressed
    # go to the sleep position

    n1.move_joints(0.0, 0.55, -1.2, 0.0, 0.0, 0.0)
    n1.set_learning_mode(True)

def clear_screen():
    os.system('cls')  # on Windows System
def position_keys():

    print("\nPosition Control Keys:   (+)      (-)\n"
          "X AXIS                    x        c\n"
          "y AXIS                    Y        u\n"
          "Z AXIS                    z        a")

if __name__ == '__main__':
    main()











