# We would recommend you run this project through PyCharm.
# PyCharm community is  free to download from their download section on their website
# Import the relevant libraries or python files that will be needed to run this code
# These are needed due to dependencies on them for functions or classes or data processing types
# This whole project runs in a virtual environment - so until it is packaged into an .exe
# We will be required to install some of the packages everytime we look to run on a new computer
# Or everytime we run it on an LSBU computer
# First and foremost navigate to the 'terminal' window at the bottom of PyCharm
# Either copy and paste the following or type it in the terminal window:
# python -m pip install --upgrade pip
# Once the latest pip installer is installed copy or type  the following:
# git clone https://github.com/LSBU-Electronics-Lab/ApiTCP_Python_NiryoOne.git
# This will add a new folder in your project called ApiTCP_Python_NiryoOne
# Right click on this folder, go to the bottom of the menu and mark directory as a sources root
# Expand the ApiTCP_Python_NiryoOne folder and find the sub-folder named niryo_one_tcp_client
# Right click on this folder, go to the bottom of  the menu and mark directory as a sources root
# Next go back to the terminal and type or copy the following
# (for each one - wait for it to finish installing before moving  on to the next):
# pip install numpy
# pip install serial
# pip install pyserial
# pip install seaborn
# pip install pandas
# pip install matplotlib
# You may get error messages saying that it could not find a version that satisfies
# If you do - dont stress - this just means that the latest version is already probably installed

# ------------ potential errors
#    You must go through and consider error handling throughout
# ------------

from niryo_one_tcp_client import *
import tkinter
from tkinter import *
from tkinter import ttk
from tkinter import messagebox
from tkinter import filedialog
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
import serial
import pandas
from serial.tools import list_ports
import math
import time
import seaborn
import PIL
from PIL import Image, ImageTk

#Create global variables - The reason why so many are being created and used, is that there was a persistent error
#occuring when trying to pass values into and out of functions. The source of the error could not be established
#however, was fixable by just declaring and working with variables as globals.
#I have a feeling that there is some kind of clash in the way the robot API handles information and the method in which
#I was attempting to pass data.
global coordinates
global ip_address
global robot_connected
global robot
global com_ports
global selected_com_port
global selected_baudrate
global arduinoData
global serial_fail_choice
global move_one_coordinates
global move_two_coordinates
global move_three_coordinates
global move_four_coordinates
global tool_arm_length
global plate_thickness
global test_data_final
global number_of_steps
global number_of_drive_pulses
global drive_distance
global update_progress
global prog_update_first_phase
global message_log

#Set non tkinter variables values where required
ip_address=''
robot_connected = False
robot = NiryoOneClient()
tool_arm_length = 0.12
test_data_final = []
message_log = []



#Create Functions

# This function takes the coordinates generated in the generate_test_data function and splits them into four sections
# The four sections are used to undertake the four stages of testing.
# The reason this is being split through a function and passing into global variables as opposed to splitting locally
# Within the relevant move functions, was due to the robots move command failing to operate when combined with the
# break-down and conditional statements of the coordinates. Through splitting it out - the problem was resolved.
def split_coordinates():
    # Even though the globals were declared at the start of the .py file - they have to be re-declared inside each
    # function, due to the functions on occasions instead creating their own local variables with the same name
    # and thereby failing to pass data out.
    global coordinates
    global move_one_coordinates
    global move_two_coordinates
    global move_three_coordinates
    global move_four_coordinates

    # Set up the four lists and declare them as lists
    move_one_coordinates = []
    move_two_coordinates = []
    move_three_coordinates =[]
    move_four_coordinates =[]

    # Now we attempt to undertake the split down of coordinates - for this a try statement is used to enable us to
    # handle an error should it occur. The most likely error is the one in which this function is called before
    # the master coordinates list has been created.
    try:
        # The structure of the coordinates tuple list is [(x, y), (x, y)....] - all we are doing here is starting an
        # itterative action where the program works through the coordinates list and identifies the first value in
        # every tuple as x - and the second as y.
        for x, y in coordinates:
            # Using if statements we can now tell it what we want it to do for each met condition
            if y <= 0.25:
                move_one_coordinates.append((x, y))
            elif 0.25 < y <= 0.5:
                move_two_coordinates.append((x, y))
            elif 0.5 < y <= 0.75:
                move_three_coordinates.append((x, y))
            elif 0.75 < y <= 1.0:
                move_four_coordinates.append((x, y))

    # Here we insert our error handling associated with the try statement. in this instance we are telling it that if
    # an error is experienced then a tkinter message box of the form showerror needs to be called and the message shown.
    except Exception as e:
        tkinter.messagebox.showerror(title='coordinate error', message=('Coordinates missing - please update and try '
                                                                       'again.'))


# This function is the one which creates the pop-up asking for the robot IP address. Additionally, it pre-inputs the
# intial elements of the ip address, based upon the typical format chosen by LSBU in their robotics laboratory.
def f_fetch_ip():

    # Within the function - we have created another function specific to this function. This nested function is called
    # at the point where we click the save button
    def ip_save():
        # We have to re-define the global to stop the function from creating a local variable with the same name.
        global ip_address

        # Here we get or fetch the current value in the entry box called ip_entry_box and assign the value to a variable
        # being created here, called ip_address
        ip_address = ip_entry_box.get()

        # Here we destroy or close down the pop-up box previously created.
        ip_window.destroy()

        # This section of code prints the input IP address in the info_frame
        # The first line defines the label, its placement in the holder info_frame and its value as the ip_address
        # variable.
        i_ip_address = tkinter.Label(info_frame, text=ip_address)
        # This second line is a geometric atribute to place it within a grid system. By assigning all elements into a
        # grid system, we are able to control where things go and how the GUI looks.
        i_ip_address.grid(row=0, column=1, padx=(20, 30), pady=(10, 5))


    default_ip="192.168.1."    # Here we create the default ip in a variable
    ip_window = tkinter.Toplevel()    # Here we create the pop-up and call it ip_window
    ip_window.title("Robot IP Address")    # This is the title of the pop-up
    ip_window.iconbitmap('robot.ico')    # This give the window our icon
    ip_window.geometry('320x100')    # This sets the size of the pop-up

    # Create the label to describe the function of the entry box and provide its geometric placement using the grid
    # system
    ip_label = tkinter.Label(ip_window, text="Enter The Robot IP Address: ")
    ip_label.grid(row=0, column=0, padx=(10, 5), pady=10)

    # Create the entry box and call it ip_entry_box. Assign it to the pop-up window.
    # Initially insert a value already defined in the variable default_ip and place this at the end (tkinter.END) of
    # any existing information within the entry box.
    # Now define the geometric position of this text entry box utilising the grid system.
    ip_entry_box = tkinter.Entry(ip_window)
    ip_entry_box.insert(tkinter.END, default_ip)
    ip_entry_box.grid(row=0, column=1, padx=(5, 10), pady=10)

    # Create a button that we call ip_save_btn, assign it to the pop-up, display the text 'Save and Close'
    # and when clicked run the function ip_save (nested inside this function).
    # Now define the geometric position of this button utilising the grid system.
    ip_save_btn = Button(ip_window, text="Save and Close", command=ip_save)
    ip_save_btn.grid(row=1, column=1, pady=10, padx=10)

    # Call the ip_window pop up defined earlier and loop until appropriately ended.
    ip_window.mainloop()

# This function is the one that looks at what is connected to the computers ports and displays the options for
# selection.
def f_fetch_port():

    # Redefine the global variables inside the function to ensure that the function doesn't create its own local
    # variables with the same names.
    global com_ports
    global selected_com_port
    global selected_baudrate

    # Use pyserial to fetch the ports list and store in com_ports variable
    com_ports = serial.tools.list_ports.comports()

    # Within the function - we have created another function specific to this function. This nested function is called
    # at the point where we click the save button
    def com_save():

        # Because we are essentially inside a new function - even though nested, we need to redeclare the global
        # variables to avoid the function creating local variables with the sname name.
        global selected_baudrate
        global selected_com_port

        # Take the user selected value from the list and attribute it to a variable called selected_port_value.
        # Split selected_port_value down by taking the first element only and assign to a variable called
        # selected_com_port.
        # Assign the value in the com_port_entry field to the variable selected_baudrate
        # After - close the pop-up window
        selected_port_value = selected_port.get()
        selected_com_port = selected_port_value.split()[0]
        selected_baudrate = int(com_baud_entry.get())
        com_window.destroy()

        # Using labels output the selected com port value and the user defined baudrate to the info_frame
        # Use the grid method to define geometric placement
        i_com_port = tkinter.Label(info_frame, text=selected_com_port)
        i_com_port.grid(row=1, column=1, padx=(20, 30), pady=(5, 5))
        i_baudrate = tkinter.Label(info_frame, text=selected_baudrate)
        i_baudrate.grid(row=2, column=1, padx=(20, 30), pady=(5, 5))

    # Create a pop-up windw that we will call com_window
    # Give it the title Arduino COM PORT, the robot icon in our folder and a geometry of 420x120 px
    com_window = tkinter.Toplevel()
    com_window.title("Arduino COM PORT")
    com_window.iconbitmap('robot.ico')
    com_window.geometry('420x120')

    #create a string variable that we can edit and set this to the output from our com_ports global variable list
    selected_port = tkinter.StringVar(com_window)
    selected_port.set(com_ports[0][0])

    # Create a default baudrate value
    default_baud = '9600'

    # Create the definition labels that the user sees on the pop-up window
    # Geometrically place these using the grid system
    com_select_label = tkinter.Label(com_window, text='Select the COM Port: ')
    com_select_label.grid(row=0, column=0, padx=(10, 5), pady=(10, 5))
    com_baud_label = tkinter.Label(com_window, text='Enter applicable Baudrate: ')
    com_baud_label.grid(row=1, column=0, padx=(10, 5), pady=(5, 5))

    # Create an options list (com_options) using the information from our com_ports list
    # Create a drop-down list, assign it to the com_window, place the selected option inside the variable named
    # selected_port, display the options in the list com_options
    # Geometrically place using the grid system
    com_options = ["{} - {}".format(port[0], port[1]) for port in com_ports]
    com_options_menu = tkinter.OptionMenu(com_window, selected_port, *com_options)
    com_options_menu.grid(row=0, column=1, padx=(5, 10), pady=(10, 5))

    # Create and entry field that we call com_baud_entry and assign it to the com_window
    # Insert our default value contained in the variable default_baud into the entry field at the end (tkinter.END) of
    # anything already in the field
    # Geometrically place using the grid system
    com_baud_entry = tkinter.Entry(com_window)
    com_baud_entry.insert(tkinter.END, default_baud)
    com_baud_entry.grid(row=1, column=1, padx=(5, 10), pady=(5, 5))

    # Create a button that we will call com_port_save_btn and assign it to the com_window
    # give our button the text Save and Close, and when clicked run the nested com_save function
    # Geometrically place using the grid system
    com_port_save_btn = tkinter.Button(com_window, text="Save and Close", command=com_save)
    com_port_save_btn.grid(row=2, column=1, padx=(20, 30), pady=(5, 10))

    # Call the com_window pop up defined earlier and loop until appropriately ended.
    com_window.mainloop()

# This function defines the actions undertaken when the user clicks the connect and calibrate button
def f_connect_attempt():

    # RE-decalre the global variables that will be used inside this function to stop them from being re-created as
    # local variables.
    global ip_address
    global robot_connected
    global selected_com_port
    global selected_baudrate
    global arduinoData
    global number_of_drive_pulses
    global drive_distance
    global serial_fail_choice


    # Define initial values for any variables as required
    number_of_drive_pulses = 0
    sleep_joints = [0.0, 0.55, -1.2, 0.0215024563846, -0.296705973, -0.070860367631]
    serial_fail_choice = True

    # Initialise a try statement to attempt a process an enable any errors to be handled effectively.
    try:

        # Update the message box with some text for the user to be given information
        update_message_box('Attempting to connect to Niryo One Robot')

        # We previously defined the name robot - now we can access the connect instructions from the API and pass the
        # ip_address string variable that we had previously collected through the function f_fetch_ip()
        # We are using the get_hardware_status command to trigger a error if the robot hasnt successfully connected
        # This is due to the discovery that the connect instruction doesnt result in an exception in the event of it
        # being unsuccessful.
        # If an exception was not caused in this step - then we set the variable robot_connected to True for later use
        robot.connect(ip_address)
        robot.get_hardware_status()
        robot_connected = True

    # This is our error handling - if an exception is caused we set the robot_connected variable to False
    # Additionally we throw up a showerror message box outlining the IP address that the connection attempt had been to
    # The reason for this is that the most likely fault to occur here is an incorrect IP address
    except Exception as e:
        robot_connected = False
        tkinter.messagebox.showerror(title='Failed to connect', message=f'Connection to to the one Niryo robot failed.'
                                                                        'Please try again. Your connection attempt was'
                                                                        f' to ip {ip_address}')

    # If the variable robot_connected is true then the following actions will occur
    if robot_connected:

        # Firstly, we throw up an askokcancel message box asking the user to remove any tooling from the robot TCP
        # The outcome from ok is True and from cancel is False
        # We have set this outcome to be held in the variable remove_tools_message
        remove_tools_message = tkinter.messagebox.askokcancel(title='Remove Tooling', message='Please ensure all tooling'
                                                                                              ' has been removed from'
                                                                                              ' the TCP before clicking '
                                                                                              ' ok. Failure to do so'
                                                                                              ' will result in damage'
                                                                                              ' to the robotic arm.',
                                                              icon='warning')

        # In this nested if statement - if the remove_tools_message is true then the following actions get undertaken
        if remove_tools_message:

            # We first attempt to send an instruction set to the robot. This instruction set is for both the arm and
            # the linear rail controls. A try statement is being used to enable us to handle any errors.
            try:

                # Firstly we inform the user of what we are doing by updating the message box
                # Then we tell the robot arm to undertake a calibration if it needs one (self-determined)
                # Once it has either checked and completed or checked and decided it doesnt need to self calibrate;
                # we update the message box to let the user know we are instructing a nod to confirm connection success
                # This is done so that in the event that the robot arm doesnt need calibration - the user sees something
                # happen and isnt left wondering if the button did anything.
                # We allow a second (the time.sleep command) for the robot to complete any movements it is undertaking
                # then we send the robot to the joints position defined in our sleep_joints variable
                # Finally we update the user to let them know that we are about to start the calibration process on the
                # linear rail.
                update_message_box('Checking if Niryo One calibration is required')
                robot.calibrate(CalibrateMode.AUTO)
                update_message_box('Telling robot to nod to confirm to user that connection succesful')
                #robot.move_pose(-.0, -0.44, 0.15, -0.041, 0.758, -1.563)
                robot.move_pose(0.15, 0., 0.2, -0.041, 0.758, -1.563)
                time.sleep(1)
                robot.move_joints(*sleep_joints)
                update_message_box('Calibration cycle starting for linear rail')

                # We develop constants to hold our constraints
                # This just makes it easier to change these variables if we need to
                steps_per_revolution = 200
                mm_per_revolution = 5
                min_pulse_width = 2.5e-6  # 2.5 microseconds
                min_pulse_delay = 5e-6  # 5 microseconds

                # Now we enable the driver with a signal
                # We will be using GPIO_1A (enum 0) for drive, GPIO_1B (enum 1) for direction and GPIO_1C (enum 2)
                # for enablement.
                # First we set the pin states for all pins (0 is input, 1 is output - from enums)
                robot.set_pin_mode(0, 1)
                robot.set_pin_mode(1, 1)
                robot.set_pin_mode(2, 1)

                # Now we enable the limit switches for feedback
                # We will be using GPIO_2A (enum 3) for voltage out signal, GPIO_2B (enum 4) for near limit input and
                # GPIO_2C (enum 5) for far limit input
                # First we set the pin states for all pins (0 is input, 1 is output - from enums)
                robot.set_pin_mode(3, 1)
                robot.set_pin_mode(4, 0)
                robot.set_pin_mode(5, 0)

                # Now we drive the enablement pulse (pin GPIO_1C enum 1) digital state low is 0 and high is 1
                robot.digital_write(1, 1)
                # Run this for a period of time (at least 5 microseconds) to ensure drive is enabled before
                # next instruction
                time.sleep(min_pulse_delay)

                # Now we drive the directional pin GPIO_1B (enum 1) to clockwise (we think this is high)
                robot.digital_write(1, 1)
                # Run the directional pulse for a minimum time before implementing the next instruction
                time.sleep(min_pulse_delay)

                # Send signal to the limit switches
                robot.digital_write(3, 1)

                # Create a variable to hold our boolean for far and near limits
                far_limit_trig = False
                near_limit_trig = False

                # Now we step the motor until the far limit switch is triggered
                # Create a loop that will continuously run until the condition has been met
                while far_limit_trig == False:
                    # Drive Pulse On (GPIO_1A is enum 0, High is enum 1)
                    robot.digital_write(0, 1)
                    # Run the pulse for the minimum pulse width
                    time.sleep(min_pulse_width)
                    # Drive Pulse Off (GPIO_1A is enum 0, High is enum 1)
                    robot.digital_write(0, 0)
                    # Run for the minimum pulse width
                    time.sleep(min_pulse_width)
                    # Check condition of far limit switch and update far_limit_trig if appropriate
                    far_limit_pin = robot.digital_read(5)
                    if far_limit_pin == 1:
                        far_limit_trig = True
                        # Now we drive the directional pin GPIO_1B (enum 1) to anti -clockwise (we think this is low)
                        robot.digital_write(1, 0)
                        # Run the directional pulse for a minimum time before implementing the next instruction
                        time.sleep(min_pulse_delay)
                        near_limit_trig = False
                    else:
                        far_limit_trig = False
                        near_limit_trig = True


                # Now that we know we have reached the far limit switch, we can work backwards to the near limits switch
                # Create a loop that will continuously run until the condition has been met
                while near_limit_trig == False:
                    # Drive Pulse On (GPIO_1A is enum 0, High is enum 1)
                    robot.digital_write(0, 1)
                    # Run the pulse for the minimum pulse width
                    time.sleep(min_pulse_width)
                    # Drive Pulse Off (GPIO_1A is enum 0, High is enum 1)
                    robot.digital_write(0, 0)
                    # Run for the minimum pulse width
                    time.sleep(min_pulse_width)
                    number_of_drive_pulses += 1
                    # Check condition of far limit switch and update far_limit_trig if appropriate
                    near_limit_trig = robot.digital_read(4)
                    if near_limit_trig == 1:
                        near_limit_trig = True
                        # Now we drive the directional pin GPIO_1B (enum 1) to clockwise (we think this is low)
                        robot.digital_write(1, 1)
                        # Run the directional pulse for a minimum time before implementing the next instruction
                        time.sleep(min_pulse_delay)
                        far_limit_trig = False
                        # Calculate distance and confirm
                        drive_revolutions = number_of_drive_pulses / steps_per_revolution
                        drive_distance = drive_revolutions * mm_per_revolution
                        update_message_box(f'linear rail drive distance:  {drive_distance}mm')
                    else:

                        pass


            # If an error occurs then we update the message box to inform the user what happened
            except Exception as e:
                update_message_box(('Failed to calibrate or undertake robot move instruction'))

        # If the user has said cancel to the 'remove tools' message then we inform them that the connect and calibrate
        # action is being cancelled until tooling is removed.
        else:
            tkinter.messagebox.showinfo(title='Abort Connection', message='Aborting Connection Attempt until '
                                                                          'confirmation of Tooling removal.')

    # This while loop will continuously run until the serial_fail_choice variable is set to False
    # This was done to enable us to graciously handle situations where the user wants to run the robot without
    # running the com port data attainment
    # The way we achieve this is by allowing the com port data attainment to result in an exception where we present
    # the user with a choice. their choice then determines whether we re-attempt connection or just pass on.
    first_data_pass_check = False

    while serial_fail_choice:

        # We use a try statement to enable us to deal with exceptions (errors) graciously
        try:

            # Firstly we update the user through the message box
            # Then we look to see if there is data being sent to the comport in question and assign this data into the
            # variable arduinoData
            # We have had to put in a hefty time delay to reduce the data collection errors that were coming through
            # from the arduino
            # Finally we update the user that the connection is successful.
            update_message_box('Attempting connection to Arduino through Serial')
            arduinoData = serial.Serial(selected_com_port, selected_baudrate)
            time.sleep(6)
            update_message_box("Serial device checked in")

            # Check to see if there is data available
            if arduinoData.inWaiting() > 0 and not first_data_pass_check:
                # Strip the data packet down to only a float
                # Read the data packet as bytes
                data_bytes = arduinoData.readline()
                # Decode the bytes to string using utf-8 and strip any newline characters
                datapacket = data_bytes.decode('utf-8').strip('\r\n')

                update_message_box(f'Received data from Serial Device: {datapacket}')

                time.sleep(3)

                first_data_pass_check = True

            update_message_box('Connection seems to have been successful')
            break

        # In our exception clause we update the user through the message box as to the failure
        # Then we offer them a choice using an askyesno messagebox which returns boolean values
        # These booleans are captured by the serial_fail_choice variable and used to determine whether the loop
        # should be continued or broken.
        except Exception as e:
            update_message_box('Connection attempt failed.')
            print(e)
            serial_fail_choice = tkinter.messagebox.askyesno(title='Serial Connection Failure', message='Connection to'
                                                                                                    ' serial was '
                                                                                                    'unsuccessful. '
                                                                                                    'Do you want to try '
                                                                                                    'again?')

            # Here we update our on-screen message box to reflect the choice that the user made
            update_message_box(f'User re-attempt connection choice: {serial_fail_choice}')

# This function is called when the user clicks the setup test button
def f_set_test():

    # Nested save function to be called after the user has input their values
    def test_save():

        # Re-define the global variables to avoid the function creating these as local variables
        global width_mm
        global length_mm
        global resolution
        global plate_thickness
        global tool_arm_length

        # Get the value from the width entry box and assign it to the width_value variable.
        # Convert the width_value to a float and assign to the width_mm variable.
        width_value = width_entry.get()
        width_mm= float(width_value)

        # Get the value from the height entry box and assign it to the length_value variable.
        # Convert the length_value to a float and assign to the length_mm variable.
        length_value= height_entry.get()
        length_mm = float(length_value)

        # Get the value from the resolution entry box and assign it to the resolution_value variable.
        # Convert the resolution_value to an integer and assign to the resolution variable.
        resolution_value = resolution_entry.get()
        resolution = int(resolution_value)

        # Get the value from the plate thickness entry box and assign it to the plate_thickness_value variable.
        # Convert the plate_thickness_value to a float, divide it by 1000 and assign to the plate_thickness variable.
        plate_thickness_value = plate_thickness_entry.get()
        plate_thickness = float(plate_thickness_value) / 1000

        # Get the value from the tool arm length entry box and assign it to the tool_arm_length_value variable.
        # Convert the tool_arm_length_value to a float, divide it by 1000 and assign to the tool_arm_length variable.
        tool_arm_length_value = tool_arm_length_entry.get()
        tool_arm_length = float(tool_arm_length_value) / 1000

        # Close down the pop-up window
        set_test_window.destroy()

        # Create a label to hold the information in the info_frame that the user has just input.
        # Geometrically place the labels using the grid method.
        i_width = tkinter.Label(info_frame, text=width_mm)
        i_width.grid(row=3, column=1, padx=(20, 30), pady=(5, 5))

        i_length = tkinter.Label(info_frame, text=length_mm)
        i_length.grid(row=4, column=1, padx=(20, 30), pady=(5, 5))

        i_resolution = tkinter.Label(info_frame, text=resolution)
        i_resolution.grid(row=5, column=1, padx=(20, 30), pady=(5, 5))

        # Call the generate_test_data function passing to it the values of width, length and resolution.
        generate_test_data(width_mm, length_mm, resolution)


    # Create the pop-up window and call it set_test_window.
    # Give the set_test_window the title of Test Piece Information.
    # Give the set_test_window the robot icon contained in the folder.
    # Set the geometric size of the set_test_window to 370x210 px.
    set_test_window = tkinter.Toplevel()
    set_test_window.title('Test Piece Information')
    set_test_window.iconbitmap('robot.ico')
    set_test_window.geometry('370x210')

    # Create the labels that go with the input boxes, and assign them to the set_test_window.
    # Geometrically place them using the grid method.
    width_label = tkinter.Label(set_test_window, text='Enter Test Piece Width in mm: ')
    width_label.grid(row=0, column=0, padx=(10, 5), pady=(10, 5))

    height_label = tkinter.Label(set_test_window, text='Enter Test Piece Length in mm: ')
    height_label.grid(row=1, column=0, padx=(10, 5), pady=(5, 5))

    resolution_label = tkinter.Label(set_test_window, text='Enter Resolution (mm/test): ')
    resolution_label.grid(row=2, column=0, padx=(10, 5), pady=(5, 10))

    plate_thickness_label = tkinter.Label(set_test_window, text='Enter plate thickness in mm: ')
    plate_thickness_label.grid(row=3, column=0, padx=(10, 5), pady=(5, 10))

    tool_arm_length_label = tkinter.Label(set_test_window, text='Enter tool arm horizontal length in mm: ')
    tool_arm_length_label.grid(row=4, column=0, padx=(10, 5), pady=(5, 10))

    # Create the input boxes and assign them to the set_test_window.
    # Geometrically place them using the grid method.
    width_entry = tkinter.Entry(set_test_window)
    width_entry.grid(row=0, column=1, padx=(5, 10), pady=(10, 5))
    width_entry.insert(0, 0)

    height_entry = tkinter.Entry(set_test_window)
    height_entry.grid(row=1, column=1, padx=(5, 10), pady=(5, 5))
    height_entry.insert(0, 0)

    resolution_entry = tkinter.Entry(set_test_window)
    resolution_entry.grid(row=2, column=1, padx=(5, 10), pady=(5, 7.5))
    resolution_entry.insert(0, 0)

    plate_thickness_entry = tkinter.Entry(set_test_window)
    plate_thickness_entry.grid(row=3, column=1, padx=(5, 10), pady=(5, 7.5))
    plate_thickness_entry.insert(0, 0)

    tool_arm_length_entry = tkinter.Entry(set_test_window)
    tool_arm_length_entry.grid(row=4, column=1, padx=(5, 10), pady=(5, 7.5))
    tool_arm_length_entry.insert(0, 120)

    # Create the Submit Button and assign it to the set_test_window.
    # Geometrically place it using the grid method.
    set_test_save_btn = tkinter.Button(set_test_window, text='Save and Close', command=test_save)
    set_test_save_btn.grid(row=5, column=1, padx=(5, 10), pady=(7.5, 10))

    # Start the loop that runs creates the window and loops until broken.
    set_test_window.mainloop()

# This function is called by f_set_test, passed width, length and resolution to generate two elements:
# The plot showing where testing will be carried out and the main coordinates list
def generate_test_data(width_mm, length_mm, resolution):

    # Re-define needed global variables to ensure that these are not recreated as local variables.
    global number_of_steps
    global coordinates

    # pre set any variables as required
    coordinates = []

    #Ensure that the contents of  the test_frame are empty before plotting to it
    for widget in test_frame.winfo_children():
        widget.destroy()

    # Create an if statement to capture the user inadvertantly setting impossible parameters
    if width_mm <= 0 or length_mm <= 0 or resolution <= 0:

        # First action is to throw up a showerror message box if the conditions are met
        size_error = tkinter.messagebox.showerror(title='Invalid Width Specified', message='Invalid prameters '
                                                                                           'specified '
                                                                                            'width and length must be '
                                                                                           'greater than'
                                                                                            ' 0. Resolution must be '
                                                                                           'greater than 0 and integer'
                                                                                           ' values. '
                                                                                           'Please update input.')

    # Else statement handles the event where the if statement is found to be false.
    else:
        # convert samples into number of data points x and y
        # Make sure the data type is an integer
        x_data_points = int(width_mm / resolution)
        y_data_points = int(width_mm / resolution)
        #resolution = math.sqrt(samples)

        # convert width and length to m
        width = width_mm / 1000
        length = length_mm / 1000

        # Because our robot sits in the centre of the piece (x-axis) - we need to adjust our coordinates
        # accordingly. This is done using the midpoint as an adjustment value
        mid_width = width / 2

        # Create a for loop that iterates through the range given by 1 to max-1
        # This is so that we have an offset from the left and right edges by at least the resolution
        # Specified by the user
        for i in range(1, x_data_points - 1):
            # Create a for loop that iterates through the range given by 1 to max-1
            # This is so that we have an offset from the top and bottom edges by at least the resolution
            # Specified by the user
            for j in range(1, y_data_points - 1):
                # Create x value in m (Niryo one only works in m) and adjust
                x_value = round((i * (resolution / 1000) - mid_width), 2)
                # Create y value in m (Niryo one only works in m)
                y_value = round((j * (resolution / 1000)), 2)
                # Append the data to the coordinates list, ensure data type is float as Niryo one only accepts float
                coordinates.append((float(x_value), float(y_value)))

        # Create the figure on which we will plot
        # Set the aspect to equal (one unit in x = one unit in y) - box tells it to adjust the plot dimensions so as to
        # be square.
        # Set a grid over the plot.
        # Use a scatter plot from the coordinates list which you unzip. Make the plot points red and size 8
        # Give the plot the title of Proposed Test, as well as naming the x and y axis.
        fig, ax = plt.subplots(figsize=(6.15, 5))
        ax.set_aspect('equal', 'box')
        ax.grid(True)
        ax.scatter(*zip(*coordinates), color='red', s=8)
        ax.set_title('Proposed Test')
        ax.set_ylabel('Length (y) Coordinates')
        ax.set_xlabel('Width (x) Coordinates')

        # Create a canvas on the test_frame to place the plot and call the canvas; canvas.
        # Place or draw the plot on the canvas
        # Geometrically place the plot using the pack method
        canvas = FigureCanvasTkAgg(fig, master=test_frame)
        canvas.draw()
        canvas.get_tk_widget().pack(side=tkinter.TOP, fill=tkinter.BOTH, expand=1)

        # Import the matplotlib toolbar, assign it to the canvas in the test frame.
        # Geometrically place the toolbar using the pack method.
        toolbar = NavigationToolbar2Tk(canvas, test_frame)
        toolbar.update()
        canvas.get_tk_widget().pack(side=tkinter.TOP, fill=tkinter.BOTH, expand=1)

        # Using the len function - find out the number of coordinates sets and assign to number_of_steps variable.
        # Update the user through outlining this information in the on-screen message box.
        number_of_steps = len(coordinates)
        update_message_box(f'the total number of test points is {number_of_steps}')

# This function is called by the user clicking the Run Test button
def f_run_test():

    # We use a try statement to enable us to catch any errors and handle them gracefully.
    try:
        # First ensure that the progress bar has been set to zero
        progress_bar.set(0)

        # Let the user know that we are breaking the movements down into stages.
        # Call on the split coordinates function to break down the coordinates.
        # We do not need to pass anything to the function or from the function as coordinates is a global variable.
        update_message_box('Splitting down coordinates into movement stages')
        split_coordinates()

        # Update the user that splitting down of coordinates was successful.
        # Update user that the first phase of movements being instructed.
        # Call on the first phase move function to undertake the first stage.
        # Update the user that the movement set is complete.
        update_message_box('First instruction set being sent to the robot')
        first_phase_move()
        update_message_box('First movement phase completed')

    # Capture any exceptions and throw up a showerror mesagebox.
    except Exception as e:
        tkinter.messagebox.showerror(title='error', message='Something went wrong. Please ensure that /n '
                                                            '1. You have connected to the robot /n'
                                                            '2. You have set up the test')

# This function is called by f_run_test in the course of conducting the test procedure
def first_phase_move():

    # Re-declare the global variables to stop the function from creating local versions
    global move_one_coordinates
    global coordinates
    global test_data_final
    global tool_arm_length
    global plate_thickness
    global number_of_steps
    global prog_update_first_phase
    global update_progress

    # Create a local variable that is needed and set its initial value
    phase_one_move_number = 0

    # Create a for loop that will itterate over the move_one_coordinates list and extract the first value in each tuple
    # as x and the second as y.
    for (x, y) in move_one_coordinates:

        # The coordinates require adjustment from the robots frame of reference to the real world.
        # Additionally, an adjustment is required to account for the tool extending beyond the TCP.
        # The following if statements attempt to capture and adjust the coordinates accordingly.
        if x != 0.0 and y > 0.0:
            angle_radians = math.atan(y / x)
            cosine_angle = math.cos(angle_radians)
            sine_angle = math.sin(angle_radians)
            x_adjustment = tool_arm_length * cosine_angle
            y_adjustment = tool_arm_length * sine_angle
            if x < 0:
                adjusted_x = x + x_adjustment
                adjusted_y = ((y - 0.41) - y_adjustment)
            else:
                adjusted_x = x - x_adjustment
                adjusted_y = ((y-0.41) + y_adjustment)
        elif (x==0) and (y!=0):
            adjusted_x = x
            adjusted_y = ((y-0.41) + tool_arm_length)
        else:
            adjusted_x = tool_arm_length
            adjusted_y = y - 0.41

        # With the coordinates having been adjusted - we can now try a robot move instruction, capturing any exceptions.
        try:

            # For each set of coordinates print a message telling the user where the robot is moving to.
            update_message_box(f'attempting to move to real x: {x} and y: {y}')
            update_message_box(f'Robot coordinates x: {adjusted_x} and y: {adjusted_y}')

            # Per the API instruction set, we pass the x, y and z coordinates in m.
            # Instead of directly attributing the values, however, we utilise variables.
            robot.move_pose(adjusted_x, adjusted_y, plate_thickness, -0.052, 0.715, -1.563)

            # We insert a break period to enable the robot to complete its move before we undertake to send the next
            # instruction set.
            time.sleep(3)

            # Here we check to see if there is data coming from the Arduinos Com Port.
            if arduinoData.inWaiting() > 0:

                # If there is data then we read the data and assign it to the variable data_bytes.
                # We then give a break to allow the system to stabilise (we have found this reduces errors).
                # Then we decode the received data and assign it to the variable datapacket.
                # Another rest period.
                # Then attribute the datapacket information to the variable sensor_value as a float.
                data_bytes = arduinoData.readline()
                time.sleep(1)
                datapacket = data_bytes.decode('utf-8').strip('\r\n')
                time.sleep(1)
                sensor_value = float(datapacket)

            # Update the user as to what the arduino data was.
            # Append to a tuples lis the x and y coordinates along with the sensor data.
            # Update the local variable to count the itteration number we are on.
            # Update the progress bar
            update_message_box(f'Sensor value reads {datapacket}')
            test_data_final.append((x, y, sensor_value))
            phase_one_move_number += 1
            prog_update_first_phase=(phase_one_move_number * 100) / number_of_steps
            update_progress.set(prog_update_first_phase)

        # Should there be an error, catch it and inform the user through a showerror messagebox
        # Additionally, print in teh GUI message box that the test failed.
        # Break the loop to stop the process.
        except Exception as e:
            tkinter.messagebox.showerror(title='test error', message='Test procedure experienced a critical '
                                                                     'failure - please retry.')
            update_message_box('Test cycle cancelled due to error')
            print(e)
            break

# This function is called by f_run_test in the course of conducting the test procedure
def second_phase_move():
    return

# This function is called by f_run_test in the course of conducting the test procedure
def third_phase_move():
    return

# This function is called by f_run_test in the course of conducting the test procedure
def fourth_phase_move():
    return

def f_save_test():

    # Re-declare global variables to stop function from creating local ones with the same names
    global test_data_final

    # Create a new window which we will call the save_dialog
    save_dialog = tkinter.Toplevel()

    # Output the data as a pandas data frame so that it can be saved to csv, call the data frame df
    df = pandas.DataFrame(test_data_final, columns=['x_coordinate', 'y_coordinate', 'sensor_value'])

    # Ask the user where to save using a filedialog
    csv_file_save = filedialog.asksaveasfilename(defaultextension=".csv", filetypes=[("CSV files", "*.csv")])

    # If the user exits or cancels then update on the message box
    if not csv_file_save:
        update_message_box("Save canceled. Exiting.")
        save_dialog.destroy()

    # Save the CSV and update to say that the file was saved
    df.to_csv(csv_file_save, index=False)

    # Close down the window once completed and update the user
    update_message_box('Test data save completed')
    update_message_box(f"Test data saved to: {csv_file_save}")
    save_dialog.destroy()

def f_load_test():

    # Create a new window which we will call the load_dialog
    load_dialog = tkinter.Toplevel()

    # Ask the user to select a CSV file using a file dialog
    csv_file_load = filedialog.askopenfilename(title="Select CSV File", filetypes=[("CSV files", "*.csv")])

    # Check if the user selected a file, if not update user and exit process
    if not csv_file_load:

        update_message_box("No file selected. Exiting.")
        load_dialog.destroy()

    else:

        # Ensure that the contents of the results_frame are empty before plotting to it
        for widget in results_frame.winfo_children():
            widget.destroy()

        # load the CSV data into a panda data frame
        df = pandas.read_csv(csv_file_load)

        # pivot the data to create a 2D array
        heatmap_data = df.pivot(index='y_coordinate', columns='x_coordinate', values='sensor_value')

        # create the heatmap using seaborn
        plt.figure(figsize=(6.15, 5))
        plt.title('Heatmap of Sensor Data')
        seaborn.heatmap(heatmap_data, cmap='coolwarm', annot=True, fmt=".1f", cbar_kws={'label': 'Sensor Values'})
        fig = plt.gcf()

        # Create a canvas on the results_frame to place the plot and call the canvas; canvas_r.
        # Place or draw the plot on the canvas
        # Geometrically place the plot using the pack method
        canvas_r = FigureCanvasTkAgg(fig, master=results_frame)
        canvas_r.draw()
        canvas_r.get_tk_widget().pack(side=tkinter.TOP, fill=tkinter.BOTH, expand=1)

        # Import the matplotlib toolbar, assign it to the canvas in the test frame.
        # Geometrically place the toolbar using the pack method.
        toolbar = NavigationToolbar2Tk(canvas_r, results_frame)
        toolbar.update()
        canvas_r.get_tk_widget().pack(side=tkinter.TOP, fill=tkinter.BOTH, expand=1)
        load_dialog.destroy()



def f_close():
    if robot_connected == False:
        close_error = tkinter.messagebox.showerror(title='No connection to close', message='There has been no'
                                                                                           ' connection established'
                                                                                           ' to close.')
    else:
        update_message_box('Closing down connection to Niryo One robot')
        sleep_joints = [0.0, 0.55, -1.2, 0.0215024563846, -0.296705973, -0.070860367631]
        # So we send the robot to the sleep_joints position
        robot.move_joints(*sleep_joints)
        # We set learning mode to true (this is what basically releases the torque in the motors)
        robot.set_learning_mode(True)
        # We disconnect from the robot
        robot.quit()
        print(message_log)

def update_message_box(message):

    # Create a message log
    global message_log
    message_log.append((message))

    # Enable the Text widget to update its contents
    message_print_box.config(state='normal')
    # Insert the new message at the end of the Text widget
    message_print_box.insert(tkinter.END, message + '\n')
    # Delete the first line of message
    num_lines = int(message_print_box.index('end-1c').split('.')[0])
    # If the number of lines exceeds 4, delete the excess lines
    if num_lines > 5:
        delete_line = num_lines - 5
        message_print_box.delete('1.0', f'{delete_line}.0')
    # Disable the Text widget to prevent user input
    # Disable the Text widget to prevent user input
    message_print_box.config(state='disabled')

def f_save_log():

    # Create a new window which we will call the save_log_dialog
    save_log_dialog = tkinter.Toplevel()

    # Ask the user to choose the file name and location
    save_log_path = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Text files", "*.txt")])

    # Check if the user canceled the dialog
    if not save_log_path:
        update_message_box("Message Log save canceled. Exiting")
        save_log_dialog.destroy()

    else:
        # Open the chosen file in write mode
        with open(save_log_path, "w") as file:
            # Iterate over the message log
            for message_tuple in message_log:
                # Extract the message from the tuple
                message = message_tuple
                # Write the message to the file
                file.write(message + "\n")

        update_message_box(f"Message log saved to: {save_log_path}")


def plot_results_from_test():

    global test_data_final

    # Ensure that the contents of the results_frame are empty before plotting to it
    for widget in results_frame.winfo_children():
        widget.destroy()

    # Convert the list of tuples into a DataFrame
    t_df = pandas.DataFrame(test_data_final, columns=['x_coordinate', 'y_coordinate', 'sensor_value'])

    # pivot the data to create a 2D array
    heatmap_data = t_df.pivot(index='y_coordinate', columns='x_coordinate', values='sensor_value')

    # create the heatmap using seaborn
    plt.figure(figsize=(6.15, 5))
    plt.title('Heatmap of Sensor Data')
    seaborn.heatmap(heatmap_data, cmap='coolwarm', annot=True, fmt=".1f", cbar_kws={'label': 'Sensor Values'})
    fig = plt.gcf()

    # Create a canvas on the results_frame to place the plot and call the canvas; canvas_r.
    # Place or draw the plot on the canvas
    # Geometrically place the plot using the pack method
    canvas_r = FigureCanvasTkAgg(fig, master=results_frame)
    canvas_r.draw()
    canvas_r.get_tk_widget().pack(side=tkinter.TOP, fill=tkinter.BOTH, expand=1)

    # Import the matplotlib toolbar, assign it to the canvas in the test frame.
    # Geometrically place the toolbar using the pack method.
    toolbar = NavigationToolbar2Tk(canvas_r, results_frame)
    toolbar.update()
    canvas_r.get_tk_widget().pack(side=tkinter.TOP, fill=tkinter.BOTH, expand=1)

    return

# Create the Root Window, we call this root and it is the main window which we operate in.
# Give the window a title, and icon and a size.
# For each column and row that we specify (grid system) - we configure it to change by 1px for every 1 px that we alter
# the main window.
root = Tk()
root.title("Robo_JCJ")
root.iconbitmap('robot.ico')
root.geometry('1330x1000')
root.columnconfigure(0, weight=1)
root.columnconfigure(1, weight=1)
root.rowconfigure(0, weight=1)
root.rowconfigure(1, weight=1)

# Create and set a tkinter variable which we will use to update the progress bar
update_progress = tkinter.IntVar()

#Create and place Frames for Widgets
menu_frame = ttk.Frame(root, width='6.4i', height='4.8i', relief='flat')
menu_frame.grid(row=0, column=0, padx=(10, 5), pady=(10, 5))

info_frame = ttk.Frame(root, width='6.4i', height='4.8i', relief='flat')
info_frame.grid(row=0, column=1, padx=(5, 10), pady=(10, 5))

test_frame = ttk.Frame(root, width='6.4i', height='4.8i', relief='flat')
test_frame.grid(row=1, column=0, padx=(10, 5), pady=(5, 10))

results_frame = ttk.Frame(root, width='6.4i', height='4.8i', relief='flat')
results_frame.grid(row=1, column=1, padx=(5, 10), pady=(5, 10))

#Create Buttons & Image that go into menu_frame
m_ip_address = Button(menu_frame, text='Assign the IP Address', width='25', justify=CENTER, command=f_fetch_ip)
m_ip_address.grid(column=0, row=0, pady=(20, 5), padx=20)

m_ardiuno_port = Button(menu_frame, text='Assign the Arduino Com Port', width='25', justify=CENTER, command=f_fetch_port)
m_ardiuno_port.grid(column=0, row=1, pady=(5, 5), padx=20)

m_connect_attempt = Button(menu_frame, text='Connect and Calibrate', width='25', justify=CENTER, command=f_connect_attempt)
m_connect_attempt.grid(column=0, row=2, pady=(5, 5), padx=20)

m_test_set = Button(menu_frame, text='Setup Test', width='25', justify=CENTER, command=f_set_test)
m_test_set.grid(row=3, column=0, pady=(5, 5), padx=20)

m_run_test = Button(menu_frame, text='Run Test', width='25', justify=CENTER, command=f_run_test)
m_run_test.grid(row=4, column=0, pady=(5, 5), padx=20)

m_save_test = Button(menu_frame, text='Save Test', width='25', justify=CENTER, command=f_save_test)
m_save_test.grid(row=5, column=0, pady=(5, 5), padx=20)

m_load_test_data = Button(menu_frame, text='Load Previous Test Data', width='25', justify=CENTER, command=f_load_test)
m_load_test_data.grid(row=6, column=0, pady=(5, 5), padx=20)

m_close = Button(menu_frame, text='Close Down Robot', width='25', justify=CENTER, command=f_close)
m_close.grid(row=7, column=0, pady=(5, 5), padx=20)

m_save_message_log = Button(menu_frame, text='Save Message Log', width='25', justify=CENTER, command=f_save_log)
m_save_message_log.grid(row=8, column=0, pady=(5, 20), padx=20)

logo_image_orig = Image.open('Robo_JCJ_Art_V2.png')
logo_image_resized = logo_image_orig.resize((300, 400), 2)
logo_image = ImageTk.PhotoImage(logo_image_resized)
logo_image_label = tkinter.Label(menu_frame, image=logo_image)
logo_image_label.grid(row=0, column=1, rowspan=9)

#info window frame
robo_ip_label = tkinter.Label(info_frame, text='Current Selected IP Address: ')
robo_ip_label.grid(row=0, column=0, padx=(30, 20), pady=(10, 5))

arduino_com_label = tkinter.Label(info_frame, text='Current Selected COM Port: ')
arduino_com_label.grid(row=1, column=0, padx=(30, 20), pady=(5, 5))

arduino_baudrate_label = tkinter.Label(info_frame, text='COM port Baudrate: ')
arduino_baudrate_label.grid(row=2, column=0, padx=(30, 20), pady=(5, 5))

piece_width_label = tkinter.Label(info_frame, text='Piece Width in mm: ')
piece_width_label.grid(row=3, column=0, padx=(30, 20), pady=(5, 5))

piece_length_label = tkinter.Label(info_frame, text='Piece Length in mm: ')
piece_length_label.grid(row=4, column=0, padx=(30, 20), pady=(5, 5))

piece_resolution_label = tkinter.Label(info_frame, text='Selected Resolution (mm / test point): ')
piece_resolution_label.grid(row=5, column=0, padx=(30, 20), pady=(5, 5))

progress_label = tkinter.Label(info_frame, text='Test progress: ')
progress_label.grid(row=6, column=0, padx=(30, 20), pady=(5, 5))

progress_bar = tkinter.ttk.Progressbar(info_frame, orient='horizontal', length=200, variable=update_progress)
progress_bar.grid(row=6, column=1, padx=(20, 30), pady=(5, 5))

message_print_box = tkinter.Text(info_frame, height=5, width=74)
message_print_box.grid(row=7, column=0, columnspan=2, padx=(10, 10), pady=(5, 5))
message_print_box.config(state='disabled')

author_names = tkinter.Label(info_frame, text='Authors: John Claridge, Johannes Hearn & Christoper Smeeth')
author_names.grid(row=8, columnspan=2, pady=(5, 10), padx=(10, 10))

# Open the window and loop through continuously looking for changes until closed.
root.mainloop()