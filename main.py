#This is the main file that will run the Maze Solver. It imports the logic and executes the app.
#CSCI-1620: Final Project Part 1
#Written By: Yusuf Hussain, 12/5/2025

from maze_logic import *


def main() -> None:
    """
    Creates a window with a fixed size and executes the Maze Solver.
    :return: None
    """
    application = QApplication([])
    window = Logic() #creates a window using the Logic class within maze_logic
    window.setFixedSize(600, 800)  #makes the window non-resizeable
    window.show()
    application.exec()


#Run the program
if __name__ == '__main__':
    main()
