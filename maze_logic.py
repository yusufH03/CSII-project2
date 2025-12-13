# This file contains all the logic for the Maze Solver app. Two Enum classes are used, Directions & Facing, which have collections of steps to solve the maze and facing directions respectively. The Logic class contains methods that handle: converting the GUI to an array, solving the maze, and changing the GUI based on user clicks. Helper methods check the next location in the maze and rotate the direction being faced. Error handling is used to ensure that the maze is solvable. The user creates a maze by clicking cells within the given grid. Once complete, the user clicks the  submit button and receives directions to solve their maze.
# CSCI-1620: Final Project-Part 2
# Written By: Yusuf Hussain, 12/9/2025
# import everything that is needed (PyQt6, the GUI file, and Enum)
from PyQt6.QtWidgets import *
from gui import *
from enum import Enum


class Directions(Enum):
    """
    Enum class that has variables for steps to solve the maze.
    """
    forward = None
    right = 1
    left = -1


class Facing(Enum):
    """
    Enum class for the facing directions while in the maze.
    """
    north = 0
    east = 1
    south = 2
    west = 3


class Logic(QMainWindow, Ui_MazeSolver):
    def __init__(self):
        super().__init__()
        self.setupUi(self)

        # class variable - how the maze looks by default
        # 0 is wall, 1 is open, 2 is end, 3 is visited
        self.default_maze = [
            [0, 1, 0, 0, 0, 0, 0, 0, ],
            [0, 1, 1, 1, 1, 1, 1, 0, ],
            [0, 1, 1, 1, 1, 1, 1, 0, ],
            [0, 1, 1, 1, 1, 1, 1, 0, ],
            [0, 1, 1, 1, 1, 1, 1, 0, ],
            [0, 1, 1, 1, 1, 1, 1, 0, ],
            [0, 1, 1, 1, 1, 1, 1, 0, ],
            [0, 0, 0, 0, 0, 0, 2, 0, ]
        ]
        # class variable - store all the buttons (maze cells) in a list
        self.editable_maze = [
            [self.c2_2, self.c2_3, self.c2_4, self.c2_5, self.c2_6, self.c2_7],
            [self.c3_2, self.c3_3, self.c3_4, self.c3_5, self.c3_6, self.c3_7],
            [self.c4_2, self.c4_3, self.c4_4, self.c4_5, self.c4_6, self.c4_7],
            [self.c5_2, self.c5_3, self.c5_4, self.c5_5, self.c5_6, self.c5_7],
            [self.c6_2, self.c6_3, self.c6_4, self.c6_5, self.c6_6, self.c6_7],
            [self.c7_2, self.c7_3, self.c7_4, self.c7_5, self.c7_6, self.c7_7],
        ]
        # class variable - directions that will be displayed once the maze is solved
        #self.instructions = ""

        # call the toggle_color method when a button/cell is clicked
        for row in self.editable_maze:
            for btn in row:
                btn.clicked.connect(lambda _, b=btn: self.toggle_color(b))
        self.submit_button.clicked.connect(self.convert)

    def toggle_color(self, button: QPushButton) -> None:
        """
        Toggle the background color of a button between default and wall colors.
        :param button: QPushButton to be changed
        :return: None
        """
        if "rgb(0, 85, 0)" in button.styleSheet():
            button.setStyleSheet("")  # turn a green/wall space white
        else:
            button.setStyleSheet("background-color: rgb(0, 85, 0);")  # turn a white/open space green

    def convert(self) -> None:
        """
        Reads the location of all open space and walls in the GUI maze and creates a list variable that matches it.
        :return: None
        """
        raw_maze = []
        for r in range(8):
            row_copy = []
            for c in range(8):
                row_copy.append(self.default_maze[r][c]) #copy default_maze to raw_maze
            raw_maze.append(row_copy)

        # iterate through the editable part of the maze (inner 6x6)
        for r in range(6):
            for c in range(6):
                button = self.editable_maze[r][c]
                styles = button.styleSheet()
                if "rgb(0, 85, 0)" in styles:
                    status = 0 # set the status to be a wall if it's a wall in the GUI
                else:
                    status = 1 # set the status as open if it's not a wall
                raw_maze[r + 1][c + 1] = status # update raw_maze
        # remove later########################################
        for row in raw_maze:
            print(row)

        try:
            how_to_solve_r = [d.name for d in self.solve_maze(Facing.south, raw_maze)[0][::-1]]
            print(how_to_solve_r)
            how_to_solve = "How to solve your maze:"
            for d in how_to_solve_r:
                if d == "forward":
                    how_to_solve += f" Move forward."
                elif d == "right":
                    how_to_solve += f" Turn right."
                elif d == "left":
                    how_to_solve += f" Turn left."
            how_to_solve += ". Congratulations, you made it out!"
            self.output_label.setText(how_to_solve) # tell the user how to solve the maze
        except Exception as e:
            print(e)
            self.output_label.setText("Maze is unsolvable. Please create a new maze and try again.")

    def solve_maze(self, facing: Facing, raw_maze: list, x: int = 0, y: int = 1) -> tuple[list[Directions], bool]:
        """
        Solves the maze if it is solvable. Starting position is always (0,1); user can't change it.
        :param x: starting x position
        :param y: starting y position
        :param raw_maze: current maze layout in a list format
        :param facing: current facing direction (N,S,E,W)
        :return: list of directions to the current x,y in reverse order; if directions are valid
        """
        print(f"{x},{y}") #remove
        # check base cases
        if raw_maze[x][y] == 0: #wall
            return [], False
        elif raw_maze[x][y] == 2: #end of maze
            return [], True
        elif raw_maze[x][y] == 3: #visited
            return [], False
        # mark which are visited
        raw_maze[x][y] = 3

        current_directions = [Directions.forward]  #last step in solving the maze is always going forward
        new_x, new_y = self.calculate_coords(facing, x, y) #next coordinates to move to
        directions, success = self.solve_maze(facing, raw_maze, new_x, new_y) #update the most current directions and their success to variables

        # Always move forward if possible, otherwise rotate clockwise once.
        if success:
            directions.extend(current_directions)  #for item in current_directions, append directions
            return directions, success
        else:
            facing = self.rotate(facing) #rotate right
            new_x, new_y = self.calculate_coords(facing, x, y) #next coordinates
            directions, success = self.solve_maze(facing, raw_maze, new_x, new_y) #update vars
            # Move forward after rotating right if possible, otherwise rotate counterclockwise once.
            if success:
                current_directions.append(Directions.right) #turn right (clockwise)
                directions.extend(current_directions) #add a right turn to current_directions
                return directions, success
            else:
                facing = self.rotate(self.rotate(facing))  # rotate 180 degrees right
                new_x, new_y = self.calculate_coords(facing, x, y) #next coordinates
                directions, success = self.solve_maze(facing, raw_maze, new_x, new_y) #update vars
                if success:
                    current_directions.append(Directions.left)  #right turn + 180 degrees = left turn
                    directions.extend(current_directions) #add a left turn to current_directions
                    return directions, success
                else:
                    return [], False #this branch of the maze is unsolvable

    def calculate_coords(self, facing: Facing, x: int, y: int, ) -> tuple[int, int]:
        """
        Calculates the coordinates of the direction being faced, ie next cell to check.
        :param facing: direction being faced
        :param x: current x position
        :param y: current y position
        :return: coordinates of the next cell to check
        """
        match facing:
            case Facing.north:
                return x - 1, y #previous row, same col
            case Facing.south:
                return x + 1, y #next row, same col
            case Facing.east:
                return x, y + 1 #same row, next col
            case Facing.west:
                return x, y - 1 #same row, previous col

    def rotate(self, facing: Facing, rotation: Directions = Directions.right) -> Facing:
        """
        Rotate the maze once by rotation. Default is to the right (clockwise).
        :param facing: direction being faced
        :param rotation: rotation direction (left or right)
        :return: new direction being faced
        """
        return Facing((facing.value + rotation.value) % 4) #see Facing and Directions classes above