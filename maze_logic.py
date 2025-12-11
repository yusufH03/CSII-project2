#This file contains the logic to run the voting app. It will allow the user to vote for one of 5 candidates on the ballot. In order to do so, the user must enter a valid voter ID, and choose a candidate. They can then view the election results. Another voter can return to the ballot afterward and cast their vote. Votes are tracked in a CSV file, and voter IDs are tracked in a text file. This program imports the auto-generated GUI file, created via Qt Designer.
#CSCI-1620: Final Project-Part 1
#Written By: Yusuf Hussain, 12/9/2025
#import everything that is needed (PyQt6, the GUI file, CSV module, and Regular Expressions module)
from PyQt6.QtCore import *
from PyQt6.QtWidgets import *

from gui import *


class Logic(QMainWindow, Ui_MazeSolver):
    def __init__(self):
        super().__init__()
        self.setupUi(self)

        # class variable - how the maze looks by default
        # 0 is wall, 1 is open, 2 is end, 3 is visited
        self.default_maze = [
            [0, 0, 0, 0, 0, 0, 0, 0,],
            [0, 1, 1, 1, 1, 1, 1, 0,],
            [0, 1, 1, 1, 1, 1, 1, 0,],
            [0, 1, 1, 1, 1, 1, 1, 0,],
            [0, 1, 1, 1, 1, 1, 1, 0,],
            [0, 1, 1, 1, 1, 1, 1, 0,],
            [0, 1, 1, 1, 1, 1, 1, 0,],
            [0, 0, 0, 0, 0, 0, 2, 0,]
        ]
        # class variable - store all the base directions
        self.directions = ["forward", "backward", "right", "left"]

        # turn a white/open space green if clicked
        self.editable_maze.buttonClicked.connect(lambda btn: self.toggle_color(btn)) # turn a white space green or a green space white when clicked


        #self.candidate1_checkBox.clicked.connect(lambda: self.enable_submit())
        #self.candidate2_checkBox.clicked.connect(lambda: self.enable_submit())
        #self.candidate3_checkBox.clicked.connect(lambda: self.enable_submit())
        #self.candidate4_checkBox.clicked.connect(lambda: self.enable_submit())
        #self.candidate5_checkBox.clicked.connect(lambda: self.enable_submit())
        # connect button presses to respective methods
        #self.submit_button.clicked.connect(lambda: self.check_ballot())
        #self.results_button.clicked.connect(lambda: self.results())
        #self.back_button.clicked.connect(lambda: self.home())


    # toggle between wall and default color
    def toggle_color(self, button):
        """
        Toggle color
        :param button:
        :return:
        """
        if button.styleSheet() == "":
            button.setStyleSheet("background-color: rgb(0, 85, 0);")
        else:
            button.setStyleSheet("")


    # convert maze to an array
    def convert(self):
        """
        Hi
        :return:
        """
        raw_maze = self.default_maze

        ###############help with this logic########################
        for row in self.editable_maze:
            for col in row:
                if self.c1_1.objectName() == f"{row+1}_{col+1}":
                    if self.c1_1.styleSheet() == "background-color: rgb(0, 85, 0);":
                        raw_maze[row][col] = 0
                    elif self.c1_1.styleSheet() == "":
                        raw_maze[row][col] = 1
        self.solve_maze(raw_maze) # once the maze in converted, call the method that solves it
        ############################################################

    # solve the maze
    def solve_maze(self, raw_maze, x=1, y=1):
        """
        Hey
        :param y:
        :param x:
        :param raw_maze:
        :return:
        """
        # start will always be at the top left
        # check base cases
        status = ' '
        current_directions = self.directions # list with the most current directions

        if raw_maze[x][y] == 0:
            status = 'wall'
            return False
        elif raw_maze[x][y] == 2:
            status = 'end'
            return True
        elif raw_maze[x][y] == 3:
            status = 'visited'
            return False
        self.output_label.setText(f"Currently in cell {x}, {y}")
        # mark which are visited
        raw_maze[x][y] = 3

##############################NEXT SEE IF THIS WORKS###################################
        # check each direction
        if x < len(raw_maze[y]) - 1 and self.solve_maze(raw_maze, x + 1, y):  # continue
            self.output_label.setText(f"continue {current_directions[0]}")
            return True
        elif x > 0 and self.solve_maze(raw_maze, x - 1, y):  # go back
            self.output_label.setText(f"go {current_directions[1]}")
            return True
        elif y < len(raw_maze) and self.solve_maze(raw_maze, x, y + 1):  # turn right
            self.output_label.setText(f"turn {current_directions[2]}")
            # shift the directions list left
            current_directions[3] = current_directions[0]
            current_directions[2] = current_directions[1]
            current_directions[1] = current_directions[2]
            current_directions[0] = current_directions[3]
            return True
        elif y > 0 and self.solve_maze(raw_maze, x, y - 1):  # turn left
            self.output_label.setText(f"turn {current_directions[3]}")
            # shift the directions right by 1
            current_directions[0] = current_directions[3]
            current_directions[1] = current_directions[2]
            current_directions[2] = current_directions[1]
            current_directions[3] = current_directions[0]
            return True
        return False
#######################################################################################


    # maybe do later
    def colors(self):
        pass