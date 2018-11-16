#!/usr/bin/env python
import os
import pickle
import sys
from tkinter import Tk, Menu


from AppGUI.PopUpWindow import ChangeDirectoryGUI
from AppComponents.User import CurrentUser
from Observers import DirectoryObserver


# Remember that this window runs in the ./AppGui folder, so any assets should be in there Naming convention by
# Google: module_name, package_name, ClassName, method_name, ExceptionName, function_name,
# GLOBAL_CONSTANT_NAME, global_var_name, instance_var_name, function_parameter_name, local_var_name.
class MainGUIApp:
    def __init__(self, window_title, window_width, window_length):

        # Window settings
        self.window = Tk()
        self.window.title(window_title)
        self.icon = os.getcwd() + '\\SEFD_logo_icon.ico'
        self.window.iconbitmap(self.icon)

        # get screen width and height
        ws = self.window.winfo_screenwidth()
        hs = self.window.winfo_screenheight()

        # calculate position x, y
        x = (ws / 2) - (window_width / 2)
        y = (hs / 2) - (window_length / 2)
        self.window.geometry('%dx%d+%d+%d' % (window_width, window_length, x, y))

        # Initialize existing or new user
        self.current_user = CurrentUser()

        # Load up saved data from pickle file
        self._pickle_file = self.current_user.get_current_directory() + "\\CurrentUser.svc"
        self.load_user_details()

        # Set current directory as user's last directory, if None then directory will be none
        self.current_directory = None

        # Set change directory window/dialog to None until initialized
        self.change_directory_dialog = None

        # Make an observer a set
        self._observers = set()

        # Add DirectoryObserver
        self.directory_observer = DirectoryObserver.CurrentDirectoryObserver()
        self.attach_observer(self.directory_observer)

        # Update DirectoryObserver
        self._notify_observer()


        # Set main menu bar and home page
        self.main_menu_bar()
        # self.home_page()

        # self.change_directory_dialog.closeEvent(self.update_from_observer())

    # def home_page(self):
    #     quit_button = QtGui.QPushButton("Quit", self)
    #     quit_button.clicked[bool].connect(self.close_application)
    #     quit_button.resize(quit_button.minimumSizeHint())
    #     quit_button.move(0, 0)
    #     self.show()

    def main_menu_bar(self):
        menu_bar = Menu(self.window)
        file_menu = Menu(menu_bar, tearoff=False)
        menu_bar.add_cascade(label="File", menu=file_menu)
        file_menu.add_command(label="Change Directory", command=self.show_change_directory_gui)
        file_menu.add_command(label="Quit!", command=self.close_application())

        # display the menu
        self.window.config(menu=menu_bar)
        # root.config(menu=menubar)
        # menu_bar = root.Menu(self.window.master)
        # roo.fram.master.config(menu=menu_bar)
        #

        # Quit the application
        # file_menu.add_command(label="Exit", command=self.onExit)
        #
        # quit_app_action.setShortcut("Ctrl+Q")
        # quit_app_action.setStatusTip('Save and quit the application')
        # quit_app_action.triggered.connect(self.close_application)

        # Change directory to save your files
        # change_dir_action = QtGui.QAction("&Change Directory", self)
        # change_dir_action.setShortcut("Ctrl+P")
        # change_dir_action.setStatusTip('Choose where to save your files')
        # change_dir_action.triggered.connect(self.show_change_directory_gui)
        #
        # file_menu.addAction(change_dir_action)
        # file_menu.addAction(quit_app_action)

        # self.show()

    def show_change_directory_gui(self):
        # Initialize ChangeDirectoryGUI if user wants to open that window
        self.change_directory_dialog = ChangeDirectoryGUI.ChangeDirectoryGUI(directory_observer=self.directory_observer,
                                                                             window_title="Change Directory",
                                                                             window_width=400, window_length=250,
                                                                             icon_path=self.icon)

    def close_application(self):
        print("Saving and closing application.")
        self.save_user_details()
        return self.window.destroy

    def load_user_details(self):
        if os.path.isfile(self._pickle_file) is True:
            with open(self._pickle_file, 'rb') as f:
                self.current_user = pickle.load(f)

        print("Loaded user settings")

    def save_user_details(self):
        self.current_user.set_current_directory(self.current_directory)
        with open(self._pickle_file, 'wb') as f:
            pickle.dump(self.current_user, f)

        print("Saved user settings")

    def attach_observer(self, observer):
        observer._subject = self
        self._observers.add(observer)

    def detach_observer(self, observer):
        observer._subject = None
        self._observers.discard(observer)

    def _notify_observer(self):
        for observer in self._observers:
            observer.update(self.current_directory)

    def update_from_observer(self):
        print("Updating from observers")
        for observer in self._observers:
            # Update our current directory from DirectoryObserver
            if observer is isinstance(observer, DirectoryObserver.CurrentDirectoryObserver):
                self.current_directory = observer.get_directory()


def main():
    main_window = MainGUIApp("SEC Edgar File Downloader", 900, 600)
    # directory_observer = DirectoryObserver.CurrentDirectoryObserver()
    # main_window.attach_observer(directory_observer)
    main_window.window.mainloop()
    # main_window.show()
    # sys.exit(app.exec_())


if __name__ == '__main__':
    main()
