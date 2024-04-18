#Check Canvas argument to establish why this is causing an instance window to remain

import tkinter
from tkinter import *
from tkinter import ttk
import serial
from serial.tools import list_ports
import test_generator

#Create Required Variables


#Create Functions
def f_fetch_ip():

    def ip_save():
        global ip_address
        ip_address = ip_entry_box.get()
        ip_window.destroy()

        i_ip_address = tkinter.Label(info_frame, text=ip_address)
        i_ip_address.grid(row=0, column=1, padx=(20, 30), pady=(20, 5))


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
    com_ports = serial.tools.list_ports.comports()

    def com_save():
        selected_port_value = selected_port.get()
        selected_com_port = selected_port_value.split()[0]
        com_window.destroy()

        i_com_port = tkinter.Label(info_frame, text=selected_com_port)
        i_com_port.grid(row=1, column=1, padx=(20, 30), pady=(5, 5))

    com_window = tkinter.Toplevel()
    com_window.title("Arduino COM PORT")
    com_window.iconbitmap('robot.ico')
    com_window.geometry('410x100')

    #create a string variable that we can edit
    selected_port = tkinter.StringVar(com_window)
    selected_port.set(com_ports[0][0])

    com_select_label = tkinter.Label(com_window, text='Select the COM Port: ')
    com_select_label.grid(row=0, column=0, padx=(10, 5), pady=10)

    com_options = ["{} - {}".format(port[0], port[1]) for port in com_ports]
    com_options_menu = tkinter.OptionMenu(com_window, selected_port, *com_options)
    com_options_menu.grid(row=0, column=1, padx=(5, 10), pady=10)

    com_port_save_btn = tkinter.Button(com_window, text="Save and Close", command=com_save)
    com_port_save_btn.grid(row=1, column=1, padx=(20, 30), pady=(20, 5))


    com_window.mainloop()

def f_connect_attempt():
    return

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

        test_generator.main(width_mm, length_mm, resolution, test_frame)

        set_test_window.destroy()

        i_width = tkinter.Label(info_frame, text=width_mm)
        i_width.grid(row=2, column=1, padx=(20, 30), pady=(5, 5))

        i_length = tkinter.Label(info_frame, text=length_mm)
        i_length.grid(row=3, column=1, padx=(20, 30), pady=(5, 5))

        i_resolution = tkinter.Label(info_frame, text=resolution)
        i_resolution.grid(row=4, column=1, padx=(20, 30), pady=(5, 5))



    set_test_window = tkinter.Toplevel()
    set_test_window.title('Test Piece Information')
    set_test_window.iconbitmap('robot.ico')
    set_test_window.geometry('340x150')

    #Create the labels
    width_label = tkinter.Label(set_test_window, text='Enter Test Piece Width in mm: ')
    width_label.grid(row=0, column=0, padx=(10, 5), pady=(10, 5))

    height_label = tkinter.Label(set_test_window, text='Enter Test Piece Length in mm: ')
    height_label.grid(row=1, column=0, padx=(10, 5), pady=(5, 5))

    resolution_label = tkinter.Label(set_test_window, text='Enter Number of Test Points: ')
    resolution_label.grid(row=2, column=0, padx=(10, 5), pady=(5, 10))

    #Create the input boxes
    width_entry = tkinter.Entry(set_test_window)
    width_entry.grid(row=0, column=1, padx=(5, 10), pady=(10, 5))

    height_entry = tkinter.Entry(set_test_window)
    height_entry.grid(row=1, column=1, padx=(5, 10), pady=(5, 5))

    resolution_entry = tkinter.Entry(set_test_window)
    resolution_entry.grid(row=2, column=1, padx=(5, 10), pady=(5, 7.5))

    #Create the Submit Button
    set_test_save_btn = tkinter.Button(set_test_window, text='Save and Close', command=test_save)
    set_test_save_btn.grid(row=3, column=1, padx=(5, 10), pady=(7.5, 10))

    set_test_window.mainloop()


def f_run_test():
    return

def f_save_test():
    return

def f_load_test():
    return

def f_close():
    return

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
robo_ip_label.grid(row=0, column=0, padx=(30, 20), pady=(20, 5))

arduino_com_label = tkinter.Label(info_frame, text='Current Selected COM Port: ')
arduino_com_label.grid(row=1, column=0, padx=(30, 20), pady=(5, 5))

piece_width_label = tkinter.Label(info_frame, text='Piece Width in mm: ')
piece_width_label.grid(row=2, column=0, padx=(30, 20), pady=(5, 5))

piece_length_label = tkinter.Label(info_frame, text='Piece Length in mm: ')
piece_length_label.grid(row=3, column=0, padx=(30, 20), pady=(5, 5))

piece_resolution_label = tkinter.Label(info_frame, text='Selected Resolution (test points): ')
piece_resolution_label.grid(row=4, column=0, padx=(30, 20), pady=(5, 5))


root.mainloop()