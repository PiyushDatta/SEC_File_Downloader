import math
import sys
import tkinter as root

from AppGUI import MainGUI
from Observers import DirectoryObserver


class ChangeDirectoryGUI:
    def __init__(self, directory_observer, window_title, window_width, window_length, icon_path):
        # Window settings
        self.window = root.Tk()
        self.window.title(window_title)

        self.window.iconbitmap(icon_path)

        # get screen width and height
        ws = self.window.winfo_screenwidth()
        hs = self.window.winfo_screenheight()

        # calculate position x, y
        x = (ws / 2) - (window_width / 2)
        y = (hs / 2) - (window_length / 2)
        self.window.geometry('%dx%d+%d+%d' % (window_width, window_length, x, y))

        # Container for putting out buttons in
        # self.container = QtGui.QWidget()
        # self.setCentralWidget(self.container)
        # self.container_lay = QtGui.QVBoxLayout()
        # self.container.setLayout(self.container_lay)

        # Input
        # self.le = QtGui.QLineEdit()
        # self.container_lay.addWidget(self.le)

        # Check the directory button
        # self.check_btn = QtGui.QPushButton("Check Directory")
        # self.container_lay.addWidget(self.check_btn)
        # self.check_btn.clicked.connect(self.print_directory_to_user)

        # Enter button
        # self.enter_btn = QtGui.QPushButton("Enter")
        # self.container_lay.addWidget(self.enter_btn)
        # self.enter_btn.clicked.connect(self.save_directory_to_current)

        # Initialize current directory as none then get update from observer
        self.current_directory = None

        # Display buttons and input bar (Qline)
        # if self.current_directory is None:
        #     self.container_lay.addWidget(QtGui.QLabel("No current directory set"))
        # else:
        #     self.container_lay.addWidget(QtGui.QLabel("Current directory: " + self.current_directory))

        # self.container_lay.addWidget(QtGui.QLabel("Directory chosen:"))
        # self.ans = QtGui.QLabel()
        # self.container_lay.addWidget(self.ans)

    # Print the directory in the window if the user wants to check what they typed in
    # def print_directory_to_user(self):
    # chosen_directory = self.le.text()
    # self.ans.setText(chosen_directory)

    # Save the inputted directory as the current working directory where are all files are stored
    # def save_directory_to_current(self):
    # self._notify_observer()
    # confirmation_messagebox = QtGui.QMessageBox()
    # self.confirmation_messagebox.about("Confirmation", "All files will be now saved to: " + str(current_directory))
    # self.confirmation_messagebox.close()

    # Close application
    def close_application(self):
        print("Closing ChangeDirectoryGUI application.")
        return self.window.destroy
