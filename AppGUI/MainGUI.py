import pickle
import sys
from PyQt4 import QtGui, QtCore
from AppGUI.PopUpWindow import ChangeDirectoryGUI

from AppComponents.User import CurrentUser


# Remember that this window runs in the ./AppGui folder, so any assets should be in there Naming convention by
# Google: module_name, package_name, ClassName, method_name, ExceptionName, function_name,
# GLOBAL_CONSTANT_NAME, global_var_name, instance_var_name, function_parameter_name, local_var_name.
class MainGUIApp(QtGui.QMainWindow):
    def __init__(self):
        super(MainGUIApp, self).__init__()

        # Window settings
        self.setGeometry(50, 50, 500, 300)
        self.setWindowTitle("SEC Edgar File Downloader")
        self.setWindowIcon(QtGui.QIcon('SEFD_logo.png'))

        # Initialize existing or new user
        self.current_user = CurrentUser()

        # Load up saved data from pickle file
        self._pickle_file = self.current_user.get_current_directory() + "//CurrentUser.svc"
        self.load_user_details()

        # Set main menu bar and home page
        self.main_menu_bar()
        self.home_page()

    def home_page(self):
        quit_button = QtGui.QPushButton("Quit", self)
        quit_button.clicked[bool].connect(self.close_application)
        quit_button.resize(quit_button.minimumSizeHint())
        quit_button.move(0, 0)
        self.show()

    def main_menu_bar(self):
        self.statusBar()

        # Quit the application
        quit_app_action = QtGui.QAction("&Save and Quit", self)
        quit_app_action.setShortcut("Ctrl+Q")
        quit_app_action.setStatusTip('Save and quit the application')
        quit_app_action.triggered.connect(self.close_application)

        # Change directory to save your files
        change_dir_action = QtGui.QAction("&Change Directory", self)
        change_dir_action.setShortcut("Ctrl+P")
        change_dir_action.setStatusTip('Choose where to save your files')
        change_dir_action.triggered.connect(self.show_change_directory_gui)

        main_menu = self.menuBar()
        file_menu = main_menu.addMenu('&File')
        file_menu.addAction(change_dir_action)
        file_menu.addAction(quit_app_action)
        self.show()

    def show_change_directory_gui(self):
        self.change_directory_dialog = ChangeDirectoryGUI.ChangeDirectoryGUI()
        self.change_directory_dialog.show()

    def close_application(self):
        print("Saving and closing application.")
        self.save_user_details()
        sys.exit()

    def load_user_details(self):
        with open(self._pickle_file, 'rb') as f:
            self.current_user = pickle.load(f)

        print("Loaded user settings")

    def save_user_details(self):
        with open(self._pickle_file, 'wb') as f:
            pickle.dump(self.current_user, f)

        print("Saved user settings")

    @staticmethod
    def set_current_user_directory(self, new_dir):
        if self.current_user.get_current_directory is not None:
            self.current_user.set_current_directory(new_dir)

    @staticmethod
    def get_current_user_directory(self):
        return self.current_user.get_current_directory()


def main():
    app = QtGui.QApplication(sys.argv)
    main_window = MainGUIApp()
    main_window.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
