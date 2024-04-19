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
# pip install seaborn
# pip install pandas
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
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
import serial
from serial.tools import list_ports
import math
import time

#Create Required Variables
global ip_address
ip_address=''
global robot_connected
robot_connected = False
global robot
robot = NiryoOneClient()
global com_ports
global selected_com_port
global selected_baudrate

#Create Functions
def f_fetch_ip():

    def ip_save():
        global ip_address

        ip_address = ip_entry_box.get()
        ip_window.destroy()

        i_ip_address = tkinter.Label(info_frame, text=ip_address)
        i_ip_address.grid(row=0, column=1, padx=(20, 30), pady=(10, 5))


    default_ip="192.168.1."
    ip_window = tkinter.Toplevel()
    ip_window.title("Robot IP Address")
    ip_window.iconbitmap('robot.ico')
    ip_window.geometry('320x100')

    ip_label = tkinter.Label(ip_window, text="Enter The Robot IP Address: ")
    ip_label.grid(row=0, column=0, padx=(10, 5), pady=10)

    ip_entry_box = tkinter.Entry(ip_window)
    ip_entry_box.insert(tkinter.END, default_ip)
    ip_entry_box.grid(row=0, column=1, padx=(5, 10), pady=10)

    ip_save_btn = Button(ip_window, text="Save and Close", command=ip_save)
    ip_save_btn.grid(row=1, column=1, pady=10, padx=10)

    ip_window.mainloop()

def f_fetch_port():
    global com_ports
    global selected_com_port
    global selected_baudrate
    com_ports = serial.tools.list_ports.comports()

    def com_save():
        global selected_baudrate
        global selected_com_port
        selected_port_value = selected_port.get()
        selected_com_port = selected_port_value.split()[0]
        selected_baudrate = int(com_baud_entry.get())
        com_window.destroy()

        i_com_port = tkinter.Label(info_frame, text=selected_com_port)
        i_com_port.grid(row=1, column=1, padx=(20, 30), pady=(5, 5))
        i_baudrate = tkinter.Label(info_frame, text=selected_baudrate)
        i_baudrate.grid(row=2, column=1, padx=(20, 30), pady=(5, 5))

    com_window = tkinter.Toplevel()
    com_window.title("Arduino COM PORT")
    com_window.iconbitmap('robot.ico')
    com_window.geometry('420x120')

    #create a string variable that we can edit
    selected_port = tkinter.StringVar(com_window)
    selected_port.set(com_ports[0][0])

    # Create a default baudrate value
    default_baud = '9600'

    com_select_label = tkinter.Label(com_window, text='Select the COM Port: ')
    com_select_label.grid(row=0, column=0, padx=(10, 5), pady=(10, 5))

    com_baud_label = tkinter.Label(com_window, text='Enter applicable Baudrate: ')
    com_baud_label.grid(row=1, column=0, padx=(10, 5), pady=(5, 5))

    com_options = ["{} - {}".format(port[0], port[1]) for port in com_ports]
    com_options_menu = tkinter.OptionMenu(com_window, selected_port, *com_options)
    com_options_menu.grid(row=0, column=1, padx=(5, 10), pady=(10, 5))

    com_baud_entry = tkinter.Entry(com_window)
    com_baud_entry.insert(tkinter.END, default_baud)
    com_baud_entry.grid(row=1, column=1, padx=(5, 10), pady=(5, 5))

    com_port_save_btn = tkinter.Button(com_window, text="Save and Close", command=com_save)
    com_port_save_btn.grid(row=2, column=1, padx=(20, 30), pady=(5, 10))


    com_window.mainloop()

def f_connect_attempt():

    global ip_address
    global robot_connected

    sleep_joints = [0.0, 0.55, -1.2, 0.0215024563846, -0.296705973, -0.070860367631]

    try:
        update_message_box('Attempting to connect to Niryo One Robot')
        robot.connect(ip_address)
        robot.get_hardware_status()
        robot_connected = True
    except Exception as e:
        robot_connected = False
        print(f'Your connection attempt was to ip {ip_address}')
        tkinter.messagebox.showerror(title='Failed to connect', message=f'Connection to to the one Niryo robot failed.'
                                                                        'Please try again. Your connection attempt was'
                                                                        f' to ip {ip_address}')

    if robot_connected:
        remove_tools_message = tkinter.messagebox.askokcancel(title='Remove Tooling', message='Please ensure all tooling'
                                                                                              ' has been removed from'
                                                                                              ' the TCP before clicking '
                                                                                              ' ok. Failure to do so'
                                                                                              ' will result in damage'
                                                                                              ' to the robotic arm.',
                                                              icon='warning')

        if remove_tools_message:
            try:
                update_message_box('Checking if calibration is required')
                robot.calibrate(CalibrateMode.AUTO)
                update_message_box('Telling robot to nod to confirm to user that connection succesful')
                #robot.move_pose(-.0, -0.44, 0.15, -0.041, 0.758, -1.563)
                robot.move_pose(0.15, 0., 0.2, -0.041, 0.758, -1.563)
                time.sleep(1)
                robot.move_joints(*sleep_joints)
            except Exception as e:
                print('Just NOPE')
        else:
            tkinter.messagebox.showinfo(title='Abort Connection', message='Aborting Connection Attempt until '
                                                                          'confirmation of Tooling removal.')



def f_set_test():

    def test_save():
        global width_mm
        global length_mm
        global resolution

        width_value = width_entry.get()
        width_mm= float(width_value)

        length_value= height_entry.get()
        length_mm = float(length_value)

        resolution_value = resolution_entry.get()
        resolution = int(resolution_value)

        set_test_window.destroy()

        i_width = tkinter.Label(info_frame, text=width_mm)
        i_width.grid(row=3, column=1, padx=(20, 30), pady=(5, 5))

        i_length = tkinter.Label(info_frame, text=length_mm)
        i_length.grid(row=4, column=1, padx=(20, 30), pady=(5, 5))

        i_resolution = tkinter.Label(info_frame, text=resolution)
        i_resolution.grid(row=5, column=1, padx=(20, 30), pady=(5, 5))

        generate_test_data(width_mm, length_mm, resolution)



    set_test_window = tkinter.Toplevel()
    set_test_window.title('Test Piece Information')
    set_test_window.iconbitmap('robot.ico')
    set_test_window.geometry('340x150')

    #Create the labels
    width_label = tkinter.Label(set_test_window, text='Enter Test Piece Width in mm: ')
    width_label.grid(row=0, column=0, padx=(10, 5), pady=(10, 5))

    height_label = tkinter.Label(set_test_window, text='Enter Test Piece Length in mm: ')
    height_label.grid(row=1, column=0, padx=(10, 5), pady=(5, 5))

    resolution_label = tkinter.Label(set_test_window, text='Enter Resolution (mm/test): ')
    resolution_label.grid(row=2, column=0, padx=(10, 5), pady=(5, 10))

    #Create the input boxes
    width_entry = tkinter.Entry(set_test_window)
    width_entry.grid(row=0, column=1, padx=(5, 10), pady=(10, 5))
    width_entry.insert(0, 0)

    height_entry = tkinter.Entry(set_test_window)
    height_entry.grid(row=1, column=1, padx=(5, 10), pady=(5, 5))
    height_entry.insert(0, 0)

    resolution_entry = tkinter.Entry(set_test_window)
    resolution_entry.grid(row=2, column=1, padx=(5, 10), pady=(5, 7.5))
    resolution_entry.insert(0, 0)

    #Create the Submit Button
    set_test_save_btn = tkinter.Button(set_test_window, text='Save and Close', command=test_save)
    set_test_save_btn.grid(row=3, column=1, padx=(5, 10), pady=(7.5, 10))

    set_test_window.mainloop()

def generate_test_data(width_mm, length_mm, resolution):
    #Ensure that the contents of  the test_frame are empty before plotting to it
    for widget in test_frame.winfo_children():
        widget.destroy()

    # declare some globals
    global coordinates
    coordinates = []

    # error handling
    if width_mm <= 0 or length_mm <= 0 or resolution <= 0:
        size_error = tkinter.messagebox.showerror(title='Invalid Width Specified', message='Invalid prameters '
                                                                                           'specified '
                                                                                            'width and length must be '
                                                                                           'greater than'
                                                                                            ' 0. Resolution must be '
                                                                                           'greater than 0 and integer'
                                                                                           ' values. '
                                                                                           'Please update input.')
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
                
        fig, ax = plt.subplots()
        ax.set_aspect('equal', 'box')
        ax.grid(True)
        ax.scatter(*zip(*coordinates), color='red', s=8)
        ax.set_title('Proposed Test')
        ax.set_ylabel('Length (y) Coordinates')
        ax.set_xlabel('Width (x) Coordinates')

        canvas = FigureCanvasTkAgg(fig, master=test_frame)
        canvas.draw()
        canvas.get_tk_widget().pack(side=tkinter.TOP, fill=tkinter.BOTH, expand=1)

        toolbar = NavigationToolbar2Tk(canvas, test_frame)
        toolbar.update()
        canvas.get_tk_widget().pack(side=tkinter.TOP, fill=tkinter.BOTH, expand=1)

def update_progress(prog_val):
    progress_bar['value'] = prog_val

def f_run_test():
    update_message_box('Blar Blar')
    return

def f_save_test():
    return

def f_load_test():
    return

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

def update_message_box(message):
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


#Create the Root Window
root = Tk()
root.title("Robo_JCJ")
root.iconbitmap('robot.ico')
root.columnconfigure(0, weight=1)
root.columnconfigure(1, weight=1)
root.rowconfigure(0, weight=1)
root.rowconfigure(1, weight=1)

#Create and place Frames for Widgets
menu_frame = ttk.Frame(root, width='6.4i', height='4.8i', relief='groove')
menu_frame.grid(row=0, column=0, padx=(10, 5), pady=(10, 5))

info_frame = ttk.Frame(root, width='6.4i', height='4.8i', relief='groove')
info_frame.grid(row=0, column=1, padx=(5, 10), pady=(10, 5))

test_frame = ttk.Frame(root, width='6.4i', height='4.8i', relief='groove')
test_frame.grid(row=1, column=0, padx=(10, 5), pady=(5, 10))

results_frame = ttk.Frame(root, width='6.4i', height='4.8i', relief='groove')
results_frame.grid(row=1, column=1, padx=(5, 10), pady=(5, 10))

#Create Buttons that go into menu_frame
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

m_close = Button(menu_frame, text='Close Down', width='25', justify=CENTER, command=f_close)
m_close.grid(row=7, column=0, pady=(5, 20), padx=20)

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

piece_resolution_label = tkinter.Label(info_frame, text='Selected Resolution (test points): ')
piece_resolution_label.grid(row=5, column=0, padx=(30, 20), pady=(5, 5))

progress_label = tkinter.Label(info_frame, text='Test progress: ')
progress_label.grid(row=6, column=0, padx=(30, 20), pady=(5, 5))

progress_bar = tkinter.ttk.Progressbar(info_frame, orient='horizontal', length=200, mode='determinate')
progress_bar.grid(row=6, column=1, padx=(20, 30), pady=(5, 5))

message_print_box = tkinter.Text(info_frame, height=5, width=53)
message_print_box.grid(row=7, column=0, columnspan=2, padx=(30, 30), pady=(5, 10))
message_print_box.config(state='disabled')

root.mainloop()
