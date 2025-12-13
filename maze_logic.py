# T
# CSCI-1620: Final Project-Part 1
# Written By: Yusuf Hussain, 12/9/2025
# import everything that is needed (PyQt6, the GUI file, CSV module, and Regular Expressions module)

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
        # class variable - store all the base directions
        self.directions = ["forward", "backward", "right", "left"]
        # class variable - store all the buttons in a list
        self.editable_maze = [
            [self.c2_2, self.c2_3, self.c2_4, self.c2_5, self.c2_6, self.c2_7],
            [self.c3_2, self.c3_3, self.c3_4, self.c3_5, self.c3_6, self.c3_7],
            [self.c4_2, self.c4_3, self.c4_4, self.c4_5, self.c4_6, self.c4_7],
            [self.c5_2, self.c5_3, self.c5_4, self.c5_5, self.c5_6, self.c5_7],
            [self.c6_2, self.c6_3, self.c6_4, self.c6_5, self.c6_6, self.c6_7],
            [self.c7_2, self.c7_3, self.c7_4, self.c7_5, self.c7_6, self.c7_7],
        ]
        # class variable - directions that will be displayed
        #self.instructions = ""

        # call the toggle_color method when a button/cell is clicked
        for row in self.editable_maze:
            for btn in row:
                btn.clicked.connect(lambda _, b=btn: self.toggle_color(b))
        self.submit_button.clicked.connect(self.convert)


    def toggle_color(self, button:QPushButton):
        """
        Toggle the background color of a button between default and wall colors.
        :param button: QPushButton to be changed
        :return: None
        """
        if "rgb(0, 85, 0)" in button.styleSheet():
            button.setStyleSheet("")  # turn a green/wall space white
        else:
            button.setStyleSheet("background-color: rgb(0, 85, 0);") # turn a white/open space green

    # convert maze to an array
    def convert(self):
        """
        Reads the location of all open space and walls in the GUI maze and creates a list variable that matches it.
        :return:
        """
        raw_maze = []
        for r in range(8):
            row_copy = []
            for c in range(8):
                row_copy.append(self.default_maze[r][c])
            raw_maze.append(row_copy)

        for r in range(6):
            for c in range(6):
                button = self.editable_maze[r][c]
                styles = button.styleSheet()
                if "rgb(0, 85, 0)" in styles:
                    status = 0
                else:
                    status = 1
                raw_maze[r+1][c+1] = status
        # remove later########################################
        for row in raw_maze:
            print(row)

        #self.solve_maze(Facing.south, raw_maze)  # pass the converted maze into the method that solves it
        try:
            print(raw_maze[0][1])
            print(raw_maze[7][6])
            ret = [d.name for d in self.solve_maze(Facing.south, raw_maze) [0][::-1]]
            print(1, ret)
        except Exception as e:
            print(e)

    # solve the maze
    def solve_maze(self, facing:Facing, raw_maze:list, x:int=0, y:int=1) -> tuple[list[Directions], bool]:
        """

        :param x: starting x position
        :param y: starting y position
        :param raw_maze: current maze layout in a list format
        :param facing: current facing direction (N,S,E,W)
        :return: list of directions, if directions are valid
        """
        # start will always be at the top left (1,2)
        status = ' '
        #current_directions = self.directions  # list with the most current directions
        print(f"{x},{y}")
        # check base cases
        if raw_maze[x][y] == 0:
            #status = 'wall'
            return [], False
        elif raw_maze[x][y] == 2:
            #status = 'end'
            return [], True
        elif raw_maze[x][y] == 3:
            #status = 'visited'
            return [], False
        self.output_label.setText(f"Currently in cell {x}, {y}")
        # mark which are visited
        raw_maze[x][y] = 3

        current_directions = [Directions.forward] # the last step in solving the maze is always going forward

        new_x, new_y = self.calculate_index(facing, x, y)
        directions, success = self.solve_maze(facing, raw_maze, new_x, new_y)

        #
        if success:
            directions.extend(current_directions) # for element in current_directions, append directions
            return directions, success
        else:
            facing = self.rotate(facing)
            new_x, new_y = self.calculate_index(facing, x, y)
            directions, success = self.solve_maze(facing, raw_maze, new_x, new_y)
            if success:
                current_directions.append(Directions.right)
                directions.extend(current_directions)
                return directions, success
            else:
                facing = self.rotate(self.rotate(facing)) # rotate 180
                new_x, new_y = self.calculate_index(facing, x, y)
                directions, success = self.solve_maze(facing, raw_maze, new_x, new_y)
                if success:
                    current_directions.append(Directions.left) # 180 degrees + right = left
                    directions.extend(current_directions)
                    return directions, success
                else:
                    return [], False




        # # move forward unless not possible
        # try:
        #     if self.solve_maze(raw_maze, x+1, y):
        #         return True
        #     if status == 'wall':
        #         try:
        #             self.solve_maze(raw_maze, x, y+1) # turn right
        #         except IndexError:
        #             pass


        # # check each direction
        # if x < len(raw_maze[y]) - 1 and self.solve_maze(raw_maze, x + 1, y):  # continue
        #     self.output_label.setText(f"continue {current_directions[0]}")
        #     return True
        # elif x > 0 and self.solve_maze(raw_maze, x - 1, y):  # go back
        #     self.output_label.setText(f"go {current_directions[1]}")
        #     return True
        # elif y < len(raw_maze) and self.solve_maze(raw_maze, x, y + 1):  # turn right
        #     self.output_label.setText(f"turn {current_directions[2]}")
        #     # shift the directions list left
        #     current_directions[3] = current_directions[0]
        #     current_directions[2] = current_directions[1]
        #     current_directions[1] = current_directions[2]
        #     current_directions[0] = current_directions[3]
        #     return True
        # elif y > 0 and self.solve_maze(raw_maze, x, y - 1):  # turn left
        #     self.output_label.setText(f"turn {current_directions[3]}")
        #     # shift the directions right by 1
        #     current_directions[0] = current_directions[3]
        #     current_directions[1] = current_directions[2]
        #     current_directions[2] = current_directions[1]
        #     current_directions[3] = current_directions[0]
        #     return True
        # return False

    def calculate_index(self, facing:Facing, x:int, y:int,) -> tuple[int, int]:
        match facing:
            case Facing.north:
                return x-1, y
            case Facing.south:
                return x+1, y
            case Facing.east:
                return x, y+1
            case Facing.west:
                return x, y-1

    def rotate(self, facing:Facing, rotation:Directions=Directions.right) -> Facing:
        return Facing((facing.value + rotation.value)%4)


    #######################################################################################

    # maybe do later
    def colors(self):
        pass
