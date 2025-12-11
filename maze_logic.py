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
        self.default_maze = [
            [0, 0, 0, 0, 0, 0, 0, 0,],
            [0, 1, 1, 1, 1, 1, 1, 0,],
            [0, 1, 1, 1, 1, 1, 1, 0,],
            [0, 1, 1, 1, 1, 1, 1, 0,],
            [0, 1, 1, 1, 1, 1, 1, 0,],
            [0, 1, 1, 1, 1, 1, 1, 0,],
            [0, 1, 1, 1, 1, 1, 1, 0,],
            [0, 0, 0, 0, 0, 0, 0, 0,]
        ]

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
        return raw_maze

    # solve the maze
    def solve_maze(self, raw_maze):
        """
        Hey
        :param raw_maze:
        :return:
        """
        pass







    # maybe do later
    def colors(self):
        pass
