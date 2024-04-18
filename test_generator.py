# First import the relevant reference libraries
# Matplotlib is the matlab 2D graphical plotter for  representation of  data
# Numpy is an efficient mathematical scientific computing library. Good for arrays and matrices
# math is a python module granting access to a very wide variety of mathematical functions
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import numpy as np
import math
import tkinter
from tkinter import *
from tkinter import ttk

# We need to  define a function that will generate the coordinate grid of our test piece
# This function will have three key attributes - width, length and resolution which need to be imported
def generate_coordinates(width, length, resolution):
    # We need to account for a situation where an error can occur through a 0 divisible
    # To account for this we use an if/else statement
    if resolution > 1:
        delta_width = width / (resolution - 1) / 2
        delta_length = length / (resolution - 1) / 2
    else:
        delta_width = 0
        delta_length = 0

    # Because the robot will sit centrally on a rail - our width is distributed equally either side
    # We are treating the axis along which this occurs as the x-axis
    # Additionally we are offsetting with the delta objects created before
    # The reason for the offset is to avoid the robot for testing right on the edges of the piece
    neg_width = -width / 2 + delta_width
    pos_width = width / 2 - delta_width
    start_length = delta_length
    end_length = length - delta_length
    # Now we need to divide the coordinates up through their  size and the resolution we want
    # We include an if/else statement to account for the situations where resolution is 0
    x = np.linspace(neg_width, pos_width, resolution) if resolution > 1 else [0]
    y = np.linspace(start_length, end_length, resolution) if resolution > 1 else [length / 2]
    # Create an array containing all the values outlined with i and j being tied in pairs
    coordinates = [(i, j) for i in x for j in y]
    # Return the value of the coordinates object
    return coordinates


# We define a function for plotting a graphical representation of the test to be run
# Ultimately we can then use this to present the user with a visual representation of
# What they have tasked the robot to do
# This can then be followed with a confirmatory input to start the testing or abort
# The function will need to import several objects created or defined elsewhere
# These objects are neg_width, pos_width, width, length & resolution
def plot_coordinates(neg_width, pos_width, width, length, resolution, test_frame):
    # When we want to plot the graphical representation - we will need the data from the
    # Previously defined function 'generate_coordinates'
    # This previously defined function will return its results into an object called coordinates
    # Again - this function will  need to import the objects width, length & resolution
    # These objects have been defined elsewhere
    coordinates = generate_coordinates(width, length, resolution)
    # So first off we need to create a figure - this is the top level container (window) which will
    # Contain our data / plot
    # Alongside this  we create an object called ax (axis) - we could have called this object anything
    # However, we have stuck with normal conventions here
    # The object ax will hold the data for the actual graphical plot (subplot)
    fig, ax = plt.subplots()
    # Next we essentially define the scale of the axis.
    # Equal states that they are 'equal' in scale
    # Box states that this is applied to the entire window
    ax.set_aspect('equal', 'box')
    # Now  we define the plot parameters
    # the format is ([lower_x_value, upper_x_value], [constant_y_value, constant_y_value], color_and_line_style)
    # k is black and the dash -means solid line
    ax.plot([neg_width, pos_width], [0, 0], 'k-')
    # Set the axis limits
    ax.set_xlim(neg_width, pos_width)
    ax.set_ylim(0, length)
    # Apply a grid
    ax.grid(True)
    # Utilise the scatter plot data function
    # *zip  just means 'unpack' - we have a complex list which we are asking it to unpack for manipulation
    # Essentially our list looks like ([x1, y1], [x2, y2], ...[xn, yn])
    # Once it has 'unpacked we end up  with: (x1, y1) which can be plotted
    # Then (x2, y2) which can be plotted all the way through to (xn, yn)
    # It essentially separates it all out
    # Color says what color you want the scatter plot points to be
    # s=8  is just a size statement; we have chosen size 8 for the scatter points
    ax.scatter(*zip(*coordinates), color='red', s=8)
    # X axis label
    plt.xlabel('x coordinates')
    # Y axis label
    plt.ylabel('y coordinates')
    # Plot title
    plt.title('Graphical representation of the test piece and resolution of testing')
    # The final command which actually puts this all together and creates the plot to see

    # Create a Tkinter canvas
    canvas = FigureCanvasTkAgg(fig, master=test_frame)
    #canvas.draw()
    #canvas.get_tk_widget().pack(fill=tkinter.BOTH, expand=True)

    return coordinates


# Here we define the function called main
# This is literally just the function that is called as the program (this is the program)
def main(width_mm, length_mm, samples, test_frame):
    # Create an object called width_mm where we take input from our user as to the width of the piece in mm
    # For this we are using a float object - this  therefore allows us to have non integer values
    #width_mm = float(input("Enter the width of the test piece in mm: "))
    # Create an object called length_mm where we take input from our user as to the length of the piece in mm
    # For this we are using a float object - this therefore allows us to have a non integer value
    #length_mm = float(input("Enter the length of the test piece in mm: "))
    # Create an object called  samples where we ask the user how many samples or test points there should be
    # For this we are using an integer object - as we cant have less than whole test points
    #samples = int(input("Enter the number of samples you want as an integer: "))

    # Now we convert our mm measurements into m - this is because the robot works in m
    # Additionally this allows us to now define the objects width and length used elsewhere
    width = width_mm / 1000
    length = length_mm / 1000
    # Here we just provide the definition for the objects neg_width and pos_width used elsewhere
    neg_width = -width / 2
    pos_width = width / 2
    # Here we define the object 'resolution' used elsewhere
    # This object needs to convert from the users 'number of samples' to
    # What this means in terms of x and y resolution (divisible)
    # however - we can only  accept whole  numbers and hence we nest inside an integer object
    resolution = int(math.sqrt(samples))

    global coordinates
    coordinates = generate_coordinates(width, length, resolution)

    # Here we just call on the function 'plot_coordinates' to run
    # We outline that it will need to import into the function the values for
    # neg_width, pos_width, width, length & resolution
    plot_coordinates(neg_width, pos_width, width, length, resolution, test_frame)
    return coordinates