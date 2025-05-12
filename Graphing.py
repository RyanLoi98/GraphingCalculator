# COURSE CPSC 231 FALL 2021
# Lecture: L01
# Name: Ryan Loi
# Date (dd/mm/yr): 10/10/21
# Description:
'''
A program created with python 3 utilizing python's turtle graphics and math library along with functions
and loops to graphically draw a user's arithmetic expression input onto a cartesian plane. The program
will also convert between calculator and pixel coordinates while performing its functions to ensure
the cartersian plane is labeled according to the user's defined ratio and in calculator coordinates. The program will also 
determine the minima and maxima of the user's expression (if there is any) and circle them as well as print their
coordinates out into the terminal. The program will also track the global minimum and maximum across all expressions
the user may enter and also report them in the terminal as well (if they exist).
'''

from math import *
import turtle

# Constants

# Constants for screen setup and drawing the AXES
BACKGROUND_COLOR = "white"
WIDTH = 800
HEIGHT = 600
AXIS_COLOR = "black"
CALC_BLNK = 0 # used as an argument to fill in a parameter (that will not be used during a calculation) in functions with multiple parameters
TICK_LENGTH = 5
LABEL_DIST_X = 25 # distance label is printed from x-axis
LABEL_DIST_Y = 15 # distance label is printed from y-axis
Y_LABEL_OFFSET = 5 # moves the y label down 5 pixels to make it more inline with the tick

# Creating a font and text size preset constant to format text printed by the turtle.
FONT = ("Arial", 10)

# Commonly used angles for turtle pointer
ZERO_DEG = 0
NINETY_DEG = 90
ONE_EIGHTY_DEG = 180
TWO_SEVENTY_DEG = 270

# Constant to double the movement distance of the turtle
DOUBLE_DIS = 2

# Constants for get_color() function, numbers assigned to the 3 colors we will be using
RED = 0     
GREEN = 1
BLUE = 2 

# total number of colors in use in the get_color() function
NUMBER_OF_COLORS = 3 

# Constant of the intervals to draw x value of the expression in order to make the curve smooth
DELTA = 0.1

# Constant for the radius used to circle an expression's minima and maxima
RADIUS = 5

# Constants for minima and maxima color
MAXIMA_COLOR = 'purple'
MINIMA_COLOR = 'orange'

# Constant for the length of an empty list
LENGTH_EMPTY_LST = 0

# Global variables
# creating global variables (so they aren't capitalized) to contain the x and y coordinates of global minimum and global maximum across all expressions, by default 
# they will start off referencing "empty" until a global maximum or minimum has been found and its x and y coordinates are stored in these variables overriding the "empty" string.

glob_min_x = "empty"
glob_min_y = "empty"
glob_max_x = "empty"
glob_max_y = "empty"



def get_color(equation_counter):
    """
    Get color for an equation based on counter of how many equations have been drawn (this is the xth equation)
    :param equation_counter: Number x, for xth equation being drawn
    :return: A string color for turtle to use
    """
         

    '''
    Since every equation is drawn in different color, alternating from red to green to blue in that particular 
    order - i.e.the first equation is drawn in red, the second in green, the third in blue then the cycle repeats
    all over again starting with red. Since this cycle occurs in multiples of 3 equations drawn, as there are 3 colors,
    if we divide the number of the current equation being drawn (counted by the equation_counter variable) by the 
    number of colors in use (number_of_colors variable) using remainder division we are left with a remainder only 
    if the numbers of equations drawn so far isn't a multiple of the numbers colors. This means the cycle of alternating
    through the 3 colors has not been completed yet, and the remainder represents the next color in the sequence
    that will be assigned to the equation that is to be drawn. 

    Example:
    
    Since we start counting from 0 (as our equation_counter starts from 0) then the following is true: 
    a) Equation #0 = red and 0 % 3 = 0 
    b) Equation #1 = green and 1 % 3 = 1 
    c) Equation # 2 = blue and 2 % 3 = 2

    --- One multiple of 3 has been completed ---
    
    d) Equation 3 = red and 3 % 3 = 0, as we can see any remainder 0 will be red, as a remainder of 0 means the equation number is a multiple of 3 and thus our cycle has repeated and our 1st color is used. 
    e) Equation 4 = green and 4 % 3 = 1, as we can see any remainder 1 will be green, as a remainder of 1 means we are 1 past our multiple of 3 so our 2nd color is used
    f) Equation 5 = blue and 5 % 3 = 2, as we can see any remainder 2 will be blue, as a remainder of 2 means we are 2 past our multiple 3 so our 3rd color is used.    
    '''
    # obtaining our remainder as the variable color_number through remainder division with the equation_counter variable (number of the current equation to be drawn)
    color_number = equation_counter % NUMBER_OF_COLORS 

    # checking to see if the remainder stored in the variable color_number matches any of the constants set for each color
    # if they match the appropriate color is returned.
    if color_number == RED:  
        return "red"

    elif color_number == GREEN:
        return "green"

    elif color_number == BLUE:
        return "blue"    
    
        
def calc_to_screen_coord(x, y, x_origin, y_origin, ratio):
    """
    Convert a calculator (x,y) to a pixel (screen_x, screen_y) based on origin location and ratio
    :param x: Calculator x
    :param y: Calculator y
    :param x_origin: Pixel x origin of pixel coordinate system
    :param y_origin: Pixel y origin of pixel coordinate system
    :param ratio: Ratio of pixel coordinate system (each 1 in calculator is worth ratio amount of pixels)
    :return: (screen_x, screen_y) pixel version of calculator (x,y)
    """
    # calculating screen_x and screen_y
    screen_x = x_origin + (ratio * x)

    screen_y = y_origin + (ratio * y)
    
    return screen_x, screen_y


def calc_minmax_x(x_origin, ratio):
    """
    Calculate smallest and largest calculator INTEGER x value to draw for a 0->WIDTH of screen
    Smallest: Convert a pixel x=0 to a calculator value and return integer floor
    Largest : Convert a pixel x=WIDTH to a calculator value and return integer ceiling
    :param x_origin: Pixel x origin of pixel coordinate system
    :param ratio: Ratio of pixel coordinate system (each 1 in calculator is worth ratio amount of pixels)
    :return: (Smallest, Largest) x value to draw for a 0->WIDTH of screen
    """
    # calculating calculator values of the smallest x (x_min) and largest value of x (x_max)
    x_min = int(floor(((-x_origin)/ratio)))

    x_max = int(ceil(((WIDTH - x_origin) / ratio)))

    # returning x_min and x_max (in that order) to the function that calls calc_minmax_x()
    return x_min, x_max


def calc_minmax_y(y_origin, ratio):
    """
    Calculate smallest and largest calculator INTEGER y value to draw for a 0->HEIGHT of screen
    Smallest: Convert a pixel y=0 to a calculator value and return integer floor
    Largest : Convert a pixel y=HEIGHT to a calculator value and return integer ceiling
    :param y_origin: Pixel y origin of pixel coordinate system
    :param ratio: Ratio of pixel coordinate system (each 1 in calculator is worth ratio amount of pixels)
    :return: (Smallest, Largest) y value to draw for a 0->HEIGHT of screen
    """
    # calculating calculator values of the smallest y (y_min) and largest value of y (y_max)
    y_min = int(floor(((-y_origin)/ratio)))

    y_max = int(ceil(((HEIGHT - y_origin) / ratio)))

    # returning y_min and y_max (in that order) to the function that calls calc_minmax_y()
    return y_min, y_max


def draw_line(pointer, screen_x1, screen_y1, screen_x2, screen_y2):
    """
    Draw a line between two pixel coordinates (screen_x_1, screen_y_1) to (screen_x_2, screen_y_2)
    :param pointer: Turtle pointer to draw with
    :param screen_x1: The pixel x of line start
    :param screen_y1: The pixel y of line start
    :param screen_x2: The pixel x of line end
    :param screen_y2: The pixel y of line end
    :return: None (just draws in turtle)
    """
    pointer.penup()
    pointer.goto(screen_x1, screen_y1)
    pointer.pendown()
    pointer.goto(screen_x2, screen_y2)     


def draw_x_axis_tick(pointer, screen_x, screen_y):
    """
    Draw an x-axis tick for location (screen_x, screen_y)
    :param pointer: Turtle pointer to draw with
    :param screen_x: The pixel x of tick location on axis
    :param screen_y: The pixel y of tick location on axis
    :return: None (just draws in turtle)
    """
    pointer.penup()
    pointer.goto(screen_x,screen_y)
    pointer.pendown()
    pointer.setheading(NINETY_DEG)
    pointer.forward(TICK_LENGTH)
    pointer.setheading(TWO_SEVENTY_DEG)
    pointer.forward(DOUBLE_DIS*TICK_LENGTH) # moving the point down 2 times the tick length in order to create the bottom half of the tick

def draw_x_axis_label(pointer, screen_x, screen_y, label_text):
    """
    Draw an x-axis label for location (screen_x, screen_y), label is label_text
    :param pointer: Turtle pointer to draw with
    :param screen_x: The pixel x of tick location on axis
    :param screen_y: The pixel y of tick location on axis
    :param label_text: The string label to draw
    :return: None (just draws in turtle)
    """
    pointer.penup()
    pointer.goto(screen_x, screen_y)
    # printing the label below the tick
    pointer.setheading(TWO_SEVENTY_DEG)
    pointer.forward(LABEL_DIST_X) # moving the label away from the tick so they don't overlap
    pointer.write(label_text, align="center", font = FONT) # writing label centered at the tick location with specified font


def draw_y_axis_tick(pointer, screen_x, screen_y):
    """
    Draw an y-axis tick for location (screen_x, screen_y)
    :param pointer: Turtle pointer to draw with
    :param screen_x: The pixel x of tick location on axis
    :param screen_y: The pixel y of tick location on axis
    :return: None (just draws in turtle)
    """
    pointer.penup()
    pointer.goto(screen_x,screen_y)
    pointer.pendown()
    pointer.setheading(ZERO_DEG)
    pointer.forward(TICK_LENGTH)
    pointer.setheading(ONE_EIGHTY_DEG)
    pointer.forward(DOUBLE_DIS * TICK_LENGTH) #moving the point down 2 times the tick length in order to create the left half of the tick


def draw_y_axis_label(pointer, screen_x, screen_y, label_text):
    """
    Draw an y-axis label for location (screen_x, screen_y), label is label_text
    :param pointer: Turtle pointer to draw with
    :param screen_x: The pixel x of tick location on axis
    :param screen_y: The pixel y of tick location on axis
    :param label_text: The string label to draw
    :return: None (just draws in turtle)
    """
    pointer.penup()
    pointer.goto(screen_x, screen_y)
    # printing the label left of the tick
    pointer.setheading(ONE_EIGHTY_DEG)
    pointer.forward(LABEL_DIST_Y) # moving the label away from the tick so they don't overlap
    pointer.setheading(TWO_SEVENTY_DEG) # offsetting the label a bit lower than the tick so it lines up better
    pointer.forward(Y_LABEL_OFFSET)
    pointer.write(label_text, align="center", font = FONT) # writing label centered at the offset tick location with specified font


def draw_x_axis(pointer, x_origin, y_origin, ratio):
    """
    Draw an x-axis centred on given origin, with given ratio
    :param pointer: Turtle pointer to draw with
    :param x_origin: Pixel x origin of pixel coordinate system
    :param y_origin: Pixel y origin of pixel coordinate system
    :param ratio: Ratio of pixel coordinate system (each 1 in calculator is worth ratio amount of pixels)
    :return: None (just draws in turtle)
    """
    # calculating the minimum and maximum integer calculator x-values
    x_min, x_max = calc_minmax_x(x_origin, ratio)

    # calculating the screen x value that would correspond to the x_min value
    # discard is an unused variable because the calc_to_screen_coord function returns two values (x,y) in that order, and we only need the X value
    # CALC_BLNK variable is used to fill in the y parameter of the calc_to_screen_coord() function, since we are not looking for a y-value 
    screen_x1, discard = calc_to_screen_coord(x_min, CALC_BLNK, x_origin, y_origin, ratio)

    # calculating the screen x value that would correspond to the x_max value
    # discard is an unused variable because the calc_to_screen_coord function returns two values (x,y) in that order, and we only need the X value
    # CALC_BLNK variable is used to fill in the y parameter of the calc_to_screen_coord() function, since we are not looking for a y-value 
    screen_x2, discard = calc_to_screen_coord(x_max, CALC_BLNK, x_origin, y_origin, ratio)

    # drawing the x-axis
    draw_line(pointer, screen_x1, y_origin, screen_x2, y_origin)

 

    # drawing the ticks and labeling the x-axis
    for x_calc in range(x_min, (x_max + 1)):  # we are adding 1 to x_max because this allows the range function to include x_max as the ending point.

        # again we use discard because this function returns 2 values and we only need 1, and we used CALC_BLNK because this function requires 2 parameters to operate
        # and we only want to calculate x.
        screen_x, discard = calc_to_screen_coord(x_calc, CALC_BLNK, x_origin, y_origin, ratio)
        # draw X-Axis ticks
        draw_x_axis_tick(pointer, screen_x, y_origin)

        # drawing X-axis label
        label_text = str(x_calc) # converting the x coordinates between x_min and x_max from integers into strings to be printed as the X-axis's label
        draw_x_axis_label(pointer, screen_x, y_origin, label_text)


def draw_y_axis(pointer, x_origin, y_origin, ratio):
    """
    Draw an y-axis centred on given origin, with given ratio
    :param pointer: Turtle pointer to draw with
    :param x_origin: Pixel x origin of pixel coordinate system
    :param y_origin: Pixel y origin of pixel coordinate system
    :param ratio: Ratio of pixel coordinate system (each 1 in calculator is worth ratio amount of pixels)
    :return: None (just draws in turtle)
    """
    # calculating the minimum and maximum integer calculator y-values
    y_min, y_max = calc_minmax_y(y_origin, ratio)

    # calculating the screen y value that would correspond to the y_min value
    # discard is an unused variable because the calc_to_screen_coord() function returns two values (x,y) in that order, and we only need the y value
    # CALC_BLNK variable is used to fill in the x parameter of the calc_to_screen_coord() function, since we are not looking for a x-value 
    discard, screen_y1 = calc_to_screen_coord(CALC_BLNK, y_min, x_origin, y_origin, ratio)

    # calculating the screen y value that would correspond to the y_max value
    # discard is an unused variable because the calc_to_screen_coord() function returns two values (x,y) in that order, and we only need the y value
    # CALC_BLNK variable is used to fill in the x parameter of the calc_to_screen_coord() function, since we are not looking for a x-value 
    discard, screen_y2 = calc_to_screen_coord(CALC_BLNK, y_max, x_origin, y_origin, ratio)

    # drawing the y-axis
    draw_line(pointer, x_origin, screen_y1, x_origin, screen_y2)

 
    # drawing the ticks and labeling the y-axis
    for y_calc in range(y_min, (y_max + 1)): # we are adding 1 to y_max because this allows the range function to include y_max as the ending point.

        # again we use discard because this function returns 2 values and we only need 1, and we used CALC_BLNK because this function requires 2 parameters to operate
        # and we only want to calculate y.
        discard, screen_y = calc_to_screen_coord(CALC_BLNK, y_calc, x_origin, y_origin, ratio)
        # draw y-Axis ticks
        draw_y_axis_tick(pointer, x_origin, screen_y)

        # drawing y-axis label
        label_text = str(y_calc) # converting the y coordinates between y_min and y_max from integers into strings to be printed as the y-axis's label
        draw_y_axis_label(pointer, x_origin, screen_y, label_text)


def draw_circle(pointer, color, x, y):
    """
    Draws a circle with a radius defined by the RADIUS constant around a 
    minima or maxima represented by the x and y coordinates, and the circle is in the color 
    specified by the color parameter.    
    :param pointer: Turtle pointer to draw with
    :param color: color to draw the circle in    
    :param x: x coordinate of the minima or maxima
    :param y: y coordinate of the minima or maxima
    :return: None (just draws in turtle)
    """
    pointer.penup()
    pointer.goto(x, y)                  # going to the circle's center coordinates
    pointer.setheading(TWO_SEVENTY_DEG) # moving the turtle away from the center of the circle by
    pointer.forward(RADIUS)             # the distance of the radius to account for the radius of the circle and where turtle starts drawing
    pointer.setheading(ZERO_DEG)        # setting the turtle to 0 degrees to account for the counter clockwise drawing direction
    pointer.pendown()
    pointer.pencolor(color)
    pointer.circle(RADIUS)

def glob_minima_maxima_loc(minima_expr_x, minima_expr_y, maxima_expr_x, maxima_expr_y):
    '''
    Determines the location of an expression's global minimum and or maximum from a list of predetermined minimas and maximas taken from said expression, 
    the function then prints the x & y coordinates of the expression's global minimum and or maximum to the terminal. 
    If the minimum and maximum do not exist the function will print that the expression doesn't have a minimum and or maximum. The
    function also tracks the smallest global minimum and or largest maximum across all functions (if they exist - if not it will print they don't exist) 
    with the use of global variables, and will also report their x and y coordinates in the terminal. 

    :param minima_expr_x: a variable referencing a list containing all of the x calculator coordinates for an expression's minimas 
    (if the expression doesn't have any maximas the list will be empty).
    :minima_expr_y: a variable referencing a list containing all of the y calculator coordinates for an expression's minimas 
    (if the expression doesn't have any maximas the list will be empty) 
    :maxima_expr_x: a variable referencing a list containing all of the x calculator coordinates for an expression's maximas 
    (if the expression doesn't have any maximas the list will be empty)
    :maxima_expr_y: a variable referencing a list containing all of the y calculator coordinates for an expression's maximas 
    (if the expression doesn't have any maximas the list will be empty)
    :return: None (just prints in the terminal)
    '''
    # accessing the global minimum and global maximum variables to keep track of these values across all expressions
    # using the global key word so this function may write to the global variables as well
    global glob_min_x
    global glob_min_y

    global glob_max_x
    global glob_max_y


    # Determining the global minimum of an expression, and the global minimum across all expressions

    if len(minima_expr_y) > LENGTH_EMPTY_LST:   # checking to see if the list of y coordinates for minimas is empty or not (hence the list length being greater the 
                                                # LENGTH_EMPTY_LIST constant which references 0), if it is the statements within the if statement triggers and we 
                                                # engage in determining the global minimum for an expression) 
      
     
        '''
        The strategy used to find the smallest minimum in an expression (thus the expression's global minimum) will be to utilize a loop and the list of y-coordinates of all of the minimas
        in an expression (minima_expr_y). Essentially we will take the first y-coordinate in the list, and compare it to every single y-coordinate in the list one by one. If a y-coordinate 
        in the list is smaller than the first we will replace the first y-coordinate with the smaller subsequent y coordinate. Then we will continue to compare that new smaller y-coordinate
        with the following y-coordinates in the list, and only replacing the y-coordinate if a smaller one is found. This will continue until the end of the list is reached, and at that point
        the y-coordinate we have will be the smallest one in the list and thus the expression's global minimum. We will also record the position in the list of where we found that y-coordinate
        and we will use that to access its corresponding x-coordinate in the list storing the x-coordinate of every minima for that same expression (minima_expr_x). Since these x and y coordinates
        are stored in order for each minima of an expression and at the same time, the same position in either list will result in the x and y coordinate that are a pair and define the same minima.
        Thus we will now have the x and y coordinate that defines the expression's global minimum, and we can print it into the terminal. Note: if an expression has multiple minima of the same 
        value (y-coordinates are the same like the expression sin(x)) then the program will pick only one of them since they are all the same.       
        '''
        # setting a variable index to 0, in order to track how many times a the while loop iterates and to access items in the list positionally
        index = 0

        minima_y = minima_expr_y[index] # accessing the first minima's y-coordinate and storing it as minima_y, this will be compared to subsequent y-coordinates of other minima's in the list
                                        # to find the expression's global minimum. This variable can be thought of as the initial or benchmark minima as we will compare it to others.    

        minima_x = minima_expr_x[index]  # storing the corresponding x-coordinate that also defines the first minima to the variable minima_x, this will be used if the minima is indeed the smallest
                                         # one within the expression
         
        index += 1  # increasing the index variable by 1, so it can positionally access the next item in the lists, and properly control the while loop.

        # looping until the index variable is less than the length of the list (which means we loop until the end of the list)
        while index < len(minima_expr_y):
            y_2 = minima_expr_y[index]  # assigning the next y - coordinate of the next minima to the variable y_2.       

            if y_2 < minima_y: # comparing if the next minima in the list is smaller than our initial minima which we use as a benchmark 
                minima_y = y_2 # if the next minima is smaller, we reassign our benchmark or initial minima variable to be the new smaller minima
                minima_x = minima_expr_x[index] # we also reassign the x-coordinate of the initial/benchmark minima variable to be the x coordinate of the new smaller minima               
                index += 1   # increasing the index variable by 1, so it can positionally access the next item in the lists, and properly control the while loop.
            
            else:   # if the next minima is not smaller we will just increase the index and restart the loop
                index += 1   # increasing the index variable by 1, so it can positionally access the next item in the lists, and properly control the while loop.
        
        print('Expression global minimum: (', minima_x, ', ', minima_y, ')', sep='') # after the loop is done, the x and y coordinates of the smallest minimum in the expression is printed

        
        # Next we will determine the global minimum across every expression ever drawn by the user. To do this we utilize global variables and conditional statements
        
        
        # First we check if the global variables that will store the x and y coordinate of a global minimum across all expressions is empty or not, this is done by seeing if the variables still 
        # reference the string "empty". If they do the variables have yet to be overwritten and this is the first global minimum the program has dealt with, and it will store
        # the coordinates of the minimum that we just determined above into the corresponding variables. We do not have to perform any checks to see if it is indeed the 
        # smallest minimum across all expressions because it is currently the only minimum found.
        if glob_min_x == "empty" and glob_min_y == "empty":
            glob_min_x = minima_x   # storing the global minimum's x coordinate
            glob_min_y = minima_y   # storing the global minimum's y coordinate

            print('The global minimum for all expressions is: (', glob_min_x, ', ', glob_min_y, ')', sep='') # printing the x and y coordinates for the global minimum across all expressions
        
        # if the global variables that store the x and y coordinates of global minimums is not empty we must check if the newly determined minimum is smaller to see if this will now be 
        # considered the new global minimum across all expressions. 
        else:  
             # check to see if the y coordinate of the minimum we just determined for an expression is less than the y coordinate of the current global minimum across all expressions
             # if it is, then we replace the x and y coordinates for the current global minimum of all expressions, which is stored in the variables glob_min_x, and glob_min_y respectively.
            if minima_y < glob_min_y:   
                glob_min_y = minima_y
                glob_min_x = minima_x
                print('The global minimum for all expressions is: (', glob_min_x, ', ', glob_min_y, ')', sep='') # printing the new x and y coordinates for the global minimum across all expressions 
            
            # if the y coordinate of the minimum we just determined for an expression is not less than the y coordinate of the global minimum across all expressions we just print
            # the x and y coordinates of the current global minimum across all expressions and do not replace these values
            else:
                print('The global minimum for all expressions is: (', glob_min_x, ', ', glob_min_y, ')', sep='')
    
    # if the list of y coordinates for minimas of an expression is empty then the expression does not have any minimas
    else: 
        print('The expression does not have a global minimum') # printing that the expression does not have a global minimum
        
        # Then we check if the global variables that will store the x and y coordinates of a global minimum across all expressions is empty or not, this is done to see if the variables still 
        # reference the string "empty", if they do the variables have yet to be overwritten and there were no previous minimum across all expressions drawn so far. Since we also do not have a
        # minimum in this expression we will print to the terminal that there is no global minimum across all expression
        if glob_min_x == "empty" and glob_min_y == "empty":
            print('There is no global minimum across all expressions')

        # if the global variables that store the x and y coordinates of a global minimum across all expressions is not empty (doesn't reference the string "empty") then we will print the x and y
        # coordinates for the global minimum across all expressions drawn so far. 
        else:
            print('The global minimum for all expressions is: (', glob_min_x, ', ', glob_min_y, ')', sep='')


# Determining the global maximum of an expression, and global maximum across all expressions, this is a near identical process (most of the code is nearly the same) with determining 
# the global minimum of an expression and across all expressions so they will be housed in the same function

    if len(maxima_expr_y) > LENGTH_EMPTY_LST:       # checking to see if the list of y coordinates for maximas is empty or not (hence the list length being greater the 
                                                    # LENGTH_EMPTY_LIST constant which references 0), if it is the statements within the if statement triggers and we 
                                                    # engage in determining the global maximum for an expression) 
       
        # resetting the index counter variable to 0 so it can be reused to track how many times the while loop iterates and to access items in the list positionally for the maxima's
        index = 0         
 
        maxima_y = maxima_expr_y[index]  # accessing the first maxima's y-coordinate and storing it as maxima_y, this will be compared to subsequent y-coordinates of other maxima's in the list
                                         # to find the expression's global maximum. This variable can be thought of as the initial or benchmark maxima as we will compare it to others.    

        maxima_x = maxima_expr_x[index]  # storing the corresponding x-coordinate that also defines the first maxima to the variable maxima_x, this will be used if the maxima is indeed the largest
                                         # one within the expression                                     

        index += 1  # increasing the index variable by 1, so it can positionally access the next item in the lists, and properly control the while loop.

        # looping until the index variable is less than the length of the list (which means we loop until the end of the list)
        while index < len(maxima_expr_y):
            y_2 = maxima_expr_y[index]   # assigning the next y - coordinate of the next maxima to the variable y_2.     

            if y_2 > maxima_y:  # comparing if the next maxima in the list is larger than our initial maxima which we use as a benchmark 
                maxima_y = y_2  # if the next maxima is larger, we reassign our benchmark or initial maxima variable to be the new larger maxima
                maxima_x = maxima_expr_x[index]  # we also reassign the x-coordinate of the initial/benchmark maxima variable to be the x coordinate of the new larger maxima

                index += 1   # increasing the index variable by 1, so it can positionally access the next item in the lists, and properly control the while loop.
            
            
            else:  # if the next maxima is not larger we will just increase the index and restart the loop
                index += 1  # increasing the index variable by 1, so it can positionally access the next item in the lists, and properly control the while loop.
        
        print('Expression global maximum: (', maxima_x, ', ', maxima_y, ')', sep='')  # after the loop is done, the x and y coordinates of the largest maximum in the expression is printed


         # Next we will determine the global maximum across every expression ever drawn by the user. To do this we utilize global variables and conditional statements


        # First we check if the global variables that will store the x and y coordinate of a global maximum across all expressions is empty or not, this is done by seeing if the variables still 
        # reference the string "empty". If they do the variables have yet to be overwritten and this is the first global maximum the program has dealt with, and it will store
        # the coordinates of the maximum that we just determined above into the corresponding variables. We do not have to perform any checks to see if it is indeed the 
        # largest maximum across all expressions because it is currently the only maximum found.
        if glob_max_x == "empty" and glob_max_y == "empty":
            glob_max_x = maxima_x   # storing the global maximum's x coordinate
            glob_max_y = maxima_y   # storing the global maximum's y coordinate

            print('The global maximum for all expressions is: (', glob_max_x, ', ', glob_max_y, ')', sep='') # printing the x and y coordinates for the global maximum across all expressions
        
        # if the global variables that store the x and y coordinates of global maximum is not empty we must check if the newly determined maximum is larger to see if this will now be 
        # considered the new global maximum across all expressions.
        else:
            # check to see if the y coordinate of the maximum we just determined for an expression is greater than the y coordinate of the current global maximum across all expressions
            # if it is, then we replace the x and y coordinates for the current global maximum of all expressions, which is stored in the variables glob_max_x, and glob_max_y respectively.
            if maxima_y > glob_max_y:
                glob_max_y = maxima_y
                glob_max_x = maxima_x
                print('The global maximum for all expressions is: (', glob_max_x, ', ', glob_max_y, ')', sep='') # printing the new x and y coordinates for the global maximum across all expressions
            

            # if the y coordinate of the maximum we just determined for an expression is not larger than the y coordinate of the global maximum across all expressions we just print
            # the x and y coordinates of the current global maximum across all expressions and do not replace these values
            else:
                print('The global maximum for all expressions is: (', glob_max_x, ', ', glob_max_y, ')', sep='')
    
    # if the list of y coordinates for maximas is empty then the expression does not have any maximas
    else: 
        print('The expression does not have a global maximum')  # printing that the expression does not have a global maximum

        # Then we check if the global variables that will store the x and y coordinates of a global maximum across all expressions is empty or not, this is done to see if the variables still 
        # reference the string "empty", if they do the variables have yet to be overwritten and there were no previous maximum across all expressions drawn so far. Since we also do not have a
        # maximum in this expression we will print to the terminal that there is no global maximum across all expression
        if glob_max_x == "empty" and glob_max_y == "empty":
            print('There is no global maximum across all expressions')

        # if the global variables that store the x and y coordinates of a global maximum across all expressions is not empty (doesn't reference the string "empty") then we will print the x and y
        # coordinates for the global maximum across all expressions drawn so far. 
        else:
            print('The global maximum for all expressions is: (', glob_max_x, ', ', glob_max_y, ')', sep='')
    



def draw_minima_maxima(pointer, x_calc_values, y_calc_values, x_origin, y_origin, ratio):    
    """
    Finds all of the minima and maxima of the expression that was just drawn using all of the expression's x and y calculator coordinates, 
    and then calls a draw circle function to draw a circle around these minima and maxima. 
    :param pointer: Turtle pointer to draw with    
    :param x_calc_values: A list containing an expression's x calculator coordinates
    :param y_calc_values: A list containing an expression's y calculator coordinates
    :param x_origin: Pixel x origin of pixel coordinate system
    :param y_origin: Pixel y origin of pixel coordinate system
    :param ratio: Ratio of pixel coordinate system (each 1 in calculator is worth ratio amount of pixels)
    :return: None (just draws in turtle)
    """  
    
    # creating lists to hold the x and y calculator coordinates for the minima's and maxima's across a particular expression 
    minima_expr_x = []
    minima_expr_y = []

    maxima_expr_x = []
    maxima_expr_y = []
    

    # determining the minima's across an expression

    '''
    To find the minima's in an expression we look for the characteristics of a minima: "a y-coordinate immediately surrounded by 2 other y-coordinates that are larger than it".
    More specifically we are looking for 3 points on the expression with x-coordinates that immediately follow each other consecutively. Then we compare the middle y-coordinate
    (the y-coordinate between the two other points) with the y-coordinate of the other two points. If the middle y-coordinate is smaller than the other two y-coordinates (meaning 
    the other two y-coordinates are larger than it) we have found a minima, if this condition doesn't hold we have not found a minima. To apply this to the entire expression we 
    would start at the x_min calculator value and "snake" our way along the expression's curve to the x_max calculator value. Snaking means we will start with the first 3 points 
    from x_min, then after testing this point we replace the x and y coordinates of the first point with the x and y coordinates of the middle point, and we would replace the 
    x and y coordinates of the middle point with the x and y coordinates of the third point, and we would replace the x and y coordinate of the third point with the x and y coordinates
    of a point right next to the third point. Essentially we are replacing points right to left, the x and y coordinates of the point to the right replaces the x and y coordinates of the point 
    to the left. So effectively we are "snaking" along the expression one point at a time to the right, and testing for minimas, this way we can never miss any minimas 
    within our x_min and x_max calculator window.
    '''
    
    # creating a variable to go control the while loop that goes through the list of y_values and to positionally access values in the list
    index = 0
 

    # assigning the first y coordinate to the y_first variable, this will be compared to a subsequent "middle" y coordinate to determine if the middle point is a minima,
    # note the index for this first y-variable will not be stored as the left most point is not important to save for later if we are "snaking" towards the right of the expression.
    # This is because we are replacing points from the right to the left, and the left most point will be discarded.
    y_first = y_calc_values[index]    

    # advancing the index variable by 1 so the while loop will read the next y coordinate in the list and properly control the while loop
    index += 1 

    # assigning the second y-coordinate to the y_second variable, this will be the "middle" y coordinate and the one we want to determine if it is a minima
    # we also store the index that references this y-coordinate, because if it is indeed the minima the index can be used to access the corresponding
    # x-coordinate that defines the minima from the x_calc_values list. Because while the expression was drawn the x and y coordinates for every point
    # on the expression was stored in order, so the first value in either x or y coordinate list defines the first point on the expression - and so on.
    y_second = y_calc_values[index]
    index_second = index 

    # advancing the index variable by 1 so the while loop will read the next y coordinate in the list and properly control the while loop
    index += 1
    
    
    '''
    Creating a while loop that will read through the entire length of the y_calc_values list so long as the index is less than the length of the list 
    meaning the entire list will be read.
    '''    
    while index < len(y_calc_values):
        
        # assigning the third y-coordinate to the y_third variable. This will be compared with the "middle" y - variable. The index for this y-variable will
        # also be stored so when we "snake" over to the right to test a new point (and this point becomes the middle point) we will have the index to access its corresponding x coordinate incase this 
        # point turns out to be the minima. 
        y_third = y_calc_values[index]
        index_third = index

        # testing to see if the y_second "middle" y-coordinate is smaller than both the first and second y-coordinates.
        if y_second < y_first and y_third > y_second:            
            x_second = x_calc_values[index_second]     # if y_second is indeed smaller than the other two y-coordinates then it
                                                       # is a minima of the expression and we determine its corresponding x-coordinate
                                                       # by using y_second's index to access it from the x_calc_values list.

            # Convert the x_second and y_second calculator coordinates of the minima to pixel coordinates so we can draw a circle around it on the screen          
            screen_x, screen_y = calc_to_screen_coord(x_second, y_second, x_origin, y_origin, ratio)
            draw_circle(pointer, MINIMA_COLOR, screen_x, screen_y) # draw a circle around the minima with the draw circle function and in the minima's circle color
            
            # storing the x and y calculator coordinates of the minima in the list for an expression's minimas so we can determine the global minimum for this expression out of all
            # the other minimas that may occur in this expression, and to use to determine the global minimum for any other expressions we may also choose to have this 
            # program draw.
            minima_expr_x.append(x_second) 
            minima_expr_y.append(y_second)                    
            
            # replacing y coordinates and index values as we prepare to "snake" over the the right of the expression

            y_first = y_second   # replacing the y coordinate of the first point with the second point        
            y_second = y_third   # replacing the y coordinate of the second point with the third point
            index_second = index_third  # replacing the second index with the third index
            
            index += 1  # advancing the index variable by 1 so the while loop will read the next y coordinate in the list
            
        
        # if the y_second "middle" y-coordinate is not smaller than both the first and third y-coordinates we reassign the y-coordinates and prepare to "snake" over to the right 
        else:
            y_first = y_second    # replacing the y coordinate of the first point with the second point         
            y_second = y_third    # replacing the y coordinate of the second point with the third point
            index_second = index_third  # replacing the second index with the third index

            index +=1  # advancing the index variable by 1 so the while loop will read the next y coordinate in the list



    # determining the maxima's across an expression (extremely similar technique to determining minimas which is why they share the same function)

    '''
    To find the maxima's in an expression we look for the characteristics of a maxima: "a y-coordinate immediately surrounded by 2 other y-coordinates that are smaller than it".
    More specifically we are looking for 3 points on the expression with x-coordinates that immediately follow each other consecutively. Then we compare the middle y-coordinate
    (the y-coordinate between the two other points) with the y-coordinate of the other two points. If the middle y-coordinate is larger than the other two y-coordinates (meaning 
    the other two y-coordinates are smaller than it) we have found a maxima, if this condition doesn't hold we have not found a maxima. To apply this to the entire expression we 
    would start at the x_min calculator value and "snake" our way along the expression's curve to the x_max calculator value. Snaking means we will start with the first 3 points 
    from x_min, then after testing this point we replace the x and y coordinates of the first point with the x and y coordinates of the middle point, and we would replace the 
    x and y coordinates of the middle point with the x and y coordinates of the third point, and we would replace the x and y coordinate of the third point with the x and y coordinates
    of a point right next to the third point. Essentially we are replacing points right to left, the x and y coordinates of the point to the right replaces the x and y coordinates of the point 
    to the left. So effectively we are "snaking" along the expression one point at a time to the right, and testing for maximas, this way we can never miss any maximas 
    within our x_min and x_max calculator window.
    '''
    
    # reseting the index variable back to zero to properly control the while loop that goes through the list of y_values and access values in a list
    index = 0
    
    
    # assigning the first y coordinate to the y_first variable, this will be compared to a subsequent "middle" y coordinate to determine if the middle point is a maxima,
    # note the index for this first y-variable will not be stored as the left most point is not important to save for later if we are "snaking" towards the right of the expression.
    # This is because we are replacing points from the right to the left, and the left most point will be discarded.
    y_first = y_calc_values[index]
     

    # advancing the index variable by 1 so the while loop will read the next y coordinate in the list
    index +=1 

    # assigning the second y-coordinate to the y_second variable, this will be the "middle" y coordinate and the one we want to determine if it is a maxima
    # we also store the index that references this y-coordinate, because if it is indeed the maxima the index can be used to access the corresponding
    # x-coordinate that defines the maxima from the x_calc_values list. Because while the expression was drawn the x and y coordinates for every point
    # on the expression was stored in order, so the first value in either x or y coordinate list defines the first point on the expression - and so on.
    y_second = y_calc_values[index]
    index_second = index

    # advancing the index variable by 1 so the while loop will read the next y coordinate in the list and properly control the while loop
    index += 1
    
    '''
    Creating a while loop that will read through the entire length of the y_calc_values list so long as the index is less than the length of the list 
    meaning the entire list will be read.
    '''          
    while index < len(y_calc_values):
        
        # assigning the third y-coordinate to the y_third variable. This will be compared with the "middle" y - variable. The index for this y-variable will
        # also be stored so when we "snake" over to the right (and this becomes the middle point) to test a new point we will have the index to access its corresponding x coordinate incase this 
        # point turns out to be the maxima in the next loop iteration. 
        y_third = y_calc_values[index]
        index_third = index

        # testing to see if the y_second "middle" y-coordinate is larger than both the first and third y-coordinates.
        if y_second > y_first and y_third < y_second:            
            x_second = x_calc_values[index_second]    # if y_second is indeed larger than the other two y-coordinates then it
                                                      # is a maxima of the expression and we determine its corresponding x-coordinate
                                                      # by using y_second's index to access it from the x_calc_values list.

            # Convert the x_second and y_second calculator coordinates of the maxima to pixel coordinates so we can draw a circle around it on the screen  
            screen_x, screen_y = calc_to_screen_coord(x_second, y_second, x_origin, y_origin, ratio)
            draw_circle(pointer, MAXIMA_COLOR, screen_x, screen_y) # draw a circle around the maxima with the draw circle function and in the maxima's circle color
            
            # storing the x and y coordinates of the maxima in the list for an expression's maximas so we can determine the global maximum for this expression out of all
            # the other maximas that may occur in this expression, and to use to determine the global maximum for any other expressions we may also choose to have this 
            # program draw.
            maxima_expr_x.append(x_second)
            maxima_expr_y.append(y_second)   

            y_first = y_second   # replacing the y coordinate of the first point with the second point  
            y_second = y_third   # replacing the y coordinate of the second point with the third point
            index_second = index_third   # replacing the second index with the third index 
            
            index +=1   # advancing the index variable by 1 so the while loop will read the next y coordinate in the list

        # if the y_second "middle" y-coordinate is not larger than both the first and third y-coordinates we reassign the y-coordinates and prepare to "snake" over to the right
        else:
            y_first = y_second   # replacing the y coordinate of the first point with the second point         
            y_second = y_third   # replacing the y coordinate of the second point with the third point
            index_second = index_third  # replacing the second index with the third index 

            index +=1    # advancing the index variable by 1 so the while loop will read the next y coordinate in the list
    
    
    # determining the expression's global maximum and minimum, along with the global minimum and maximum for all expressions drawn and to be drawn
    glob_minima_maxima_loc(minima_expr_x, minima_expr_y, maxima_expr_x, maxima_expr_y)


def draw_expression(pointer, expr, colour, x_origin, y_origin, ratio):
    """
    Determing the x and y screen coordinates of the arithmetic expression that the user specified, then drawing it onto the coordinate plane.
    :param pointer: Turtle pointer to draw with
    :param expr: The string expression to draw
    :param colour: The colour to draw the expression
    :param x_origin: Pixel x origin of pixel coordinate system
    :param y_origin: Pixel y origin of pixel coordinate system
    :param ratio: Ratio of pixel coordinate system (each 1 in calculator is worth ratio amount of pixels)
    :return: None (just draws in turtle and calls other functions to determine the minimas and maximas - if they exist)
    """
    # creating a list to store the x and y calculator values which will be used to determine the expression's minima and maxima
    x_calc_values = []
    y_calc_values = []

    # calculating the min and max x coordinates within the calculator window
    x_min, x_max = calc_minmax_x(x_origin, ratio)

    # Determining the coordinates of the first point of the user defined expression within the x_min and x_max calculator range, this point will be connected to a second point to form the curve of the user defined expression.    
    x1_expr = x_min # the first calculator x coordinate of the expression 
    y1_expr = calc(expr, x1_expr) # calculating the calculator y coordinate of a particular calculator x coordinate (x_expr) within the min and max calculator x range

    # converting the calculator coordinates into pixel coordinates
    screen_x1, screen_y1 = calc_to_screen_coord(x1_expr, y1_expr, x_origin, y_origin, ratio)

    # storing the calculator values into a list
    x_calc_values.append(x1_expr)
    y_calc_values.append(y1_expr)
    
    # priming the while loop to continuously determine the coordinates of subsequent point (to be connected to the first point) of the expression within the x_min and x_max calculator range
    x2_expr = x1_expr + DELTA # increasing the x-coordinate by delta (0.1) to find a close by second point in order to maintain smoothness of the curve when connecting the points
    
    while x2_expr <= x_max:
        y2_expr = calc(expr, x2_expr) # calculating the calculator y coordinate of a particular calculator x coordinate within the min and max calculator x range

        # converting the calculator coordinates into pixel coordinates
        screen_x2, screen_y2 = calc_to_screen_coord(x2_expr, y2_expr, x_origin, y_origin, ratio)

        # drawing the expression:
        pointer.color(colour) # drawing the curve in its designated color
        draw_line(pointer, screen_x1, screen_y1, screen_x2, screen_y2) # connecting the first point to the point that follows it

        # storing the calculator x and y values into a list (in order they are drawn) for use in determining the expression's minima and maxima
        x_calc_values.append(x2_expr)       
        y_calc_values.append(y2_expr)
        


        '''
        Reassigning screen_x1 and screen_y1 with the values of screen_x2 and screen_y2 respectively. This way when the loop reiterates
        it will determine the coordinates of a point following the point currently defined by screen_x2 and screen_y2, and then the current
        point can be used as the starting location and the new point can be used as the ending location so the draw line function to connect them
        '''
        screen_x1 = screen_x2
        screen_y1 = screen_y2

        x2_expr += DELTA # increasing the x_expr value by DELTA (0.1) to draw the expression in increasing x intervals of 0.1, this will make the curve look smooth
    

    # sending the list of x and y values of the drawn user defined expression to the calc_minima_maxima function in order to determine and draw circles around the minima and maxima of the expression
    draw_minima_maxima(pointer, x_calc_values, y_calc_values, x_origin, y_origin, ratio)



# YOU SHOULD NOT NEED TO CHANGE ANYTHING BELOW THIS LINE UNLESS YOU ARE DOING THE BONUS


def calc(expr, x):
    """
    Return y for y = expr(x)
    Example if x = 10, and expr = x**2, then y = 10**2 = 100.
    :param expr: The string expression to evaluate where x is the only variable
    :param x: The value to evaluate the expression at
    :return: y = expr(x)
    """
    return eval(expr)


def setup():
    """
    Sets the window up in turtle
    :return: None
    """
    turtle.bgcolor(BACKGROUND_COLOR)
    turtle.setup(WIDTH, HEIGHT, 0, 0)
    screen = turtle.getscreen()
    screen.screensize(WIDTH, HEIGHT)
    screen.setworldcoordinates(0, 0, WIDTH, HEIGHT)
    screen.delay(delay=0)
    pointer = turtle
    pointer.hideturtle()
    pointer.speed(0)
    pointer.up()
    return pointer


def main():
    """
    Main loop of calculator
    Gets the pixel origin location in the window and a ratio
    Loops a prompt getting expressions from user and drawing them
    :return: None
    """
    # Setup
    pointer = setup()
    # turtle.tracer(0)
    # Get configuration
    x_origin, y_origin = eval(input("Enter pixel coordinates of chart origin (x,y): "))
    ratio = int(input("Enter ratio of pixels per step: "))
    # Draw axis
    pointer.color(AXIS_COLOR)
    draw_x_axis(pointer, x_origin, y_origin, ratio)
    draw_y_axis(pointer, x_origin, y_origin, ratio)
    # turtle.update()
    # Get expressions
    print()  # create a space between the terminal input for the origin coordinates and ratio, and input for an arithmetic expression 
    expr = input("Enter an arithmetic expression: ")
    equation_counter = 0
    while expr != "":
        # Get colour and draw expression
        colour = get_color(equation_counter)
        draw_expression(pointer, expr, colour, x_origin, y_origin, ratio)
        # turtle.update()
        print()  # create a space between the terminal input for an arithmetic expression and terminal output of the minimum and maximums
        expr = input("Enter an arithmetic expression: ")
        equation_counter += 1


main()
turtle.exitonclick()
