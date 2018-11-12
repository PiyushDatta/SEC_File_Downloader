import math
import sys
from PyQt4 import QtGui, QtCore

current_directory = None


class ChangeDirectoryGUI(QtGui.QMainWindow):
    def __init__(self):
        super(ChangeDirectoryGUI, self).__init__()

        # Window settings
        self.setGeometry(50, 50, 300, 100)
        self.setWindowTitle("Change Directory")
        self.setWindowIcon(QtGui.QIcon('SEFD_logo.png'))

        # Container for putting out buttons in
        self.container = QtGui.QWidget()
        self.setCentralWidget(self.container)
        self.container_lay = QtGui.QVBoxLayout()
        self.container.setLayout(self.container_lay)

        # Input
        self.le = QtGui.QLineEdit()
        self.container_lay.addWidget(self.le)

        # Check the directory button
        self.check_btn = QtGui.QPushButton("Check Directory")
        self.container_lay.addWidget(self.check_btn)
        self.check_btn.clicked.connect(self.print_directory_to_user)

        # Enter button
        self.enter_btn = QtGui.QPushButton("Enter")
        self.container_lay.addWidget(self.enter_btn)
        self.enter_btn.clicked.connect(self.save_directory_to_current)

        # Display buttons and input bar (Qline)
        self.container_lay.addWidget(QtGui.QLabel("Current directory: "))
        self.container_lay.addWidget(QtGui.QLabel("Directory chosen:"))
        self.ans = QtGui.QLabel()
        self.container_lay.addWidget(self.ans)

        # Make an observer a set
        self._observers = set()

    def attach(self, observer):
        observer._subject = self
        self._observers.add(observer)

    def detach(self, observer):
        observer._subject = None
        self._observers.discard(observer)

    def _notify(self):
        for observer in self._observers:
            observer.update(self._directory_state)

    # Print the directory in the window if the user wants to check what they typed in
    def print_directory_to_user(self):
        chosen_directory = self.le.text()
        self.ans.setText(chosen_directory)

    # Save the inputted directory as the current working directory where are all files are stored
    def save_directory_to_current(self):
        current_directory = self.le.text()
        confirmation_messagebox = QtGui.QMessageBox
        confirmation_messagebox.about(self, "Confirmation", "All files will be now saved to: " + str(current_directory))
        confirmation_messagebox.close(self)

    # Close application
    def close_application(self):
        print("Closing application.")
        sys.exit()
