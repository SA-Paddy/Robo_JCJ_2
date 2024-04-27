
import time
from niryo_one_tcp_client import *
import keyboard

import os
#ROBOT 1EE
# POSE COORDINATES
x=0.22
y=-0.043
z=0.164
r=-0.062
p=1.535
ya=1.472
key=' '
incr=0.001 # increment value for all axes; May be changed to
           # different values for each axis
# JOINT COORDINATES
j1=-0.202
j2=-0.488
j3=-0.584
j4=0.061
j5=-0.505
j6=-1.792
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
    # activate learning mode
    #n1.set_learning_mode(True)
    # go to initial position defined above
    # FIRST MOVE TO JOINT COORDINATES AND THEN TO POSE
    n1.move_joints(j1,j2,j3,j4,j5,j6)
    n1.move_pose(x, y, z, r, p, ya)
    status,data1=n1.get_pose()
    status, data2 = n1.get_joints()

    print(data1)
    print("-----------")
    print(data2)
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











