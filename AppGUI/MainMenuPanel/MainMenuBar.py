import os
import pickle
import tkinter as tk
from tkinter import messagebox

from AppGUI.MainMenuPanel.MainMenuBarController import MainMenuController
from AppGUI.PopUpWindow import ChangeDirectoryGUI
from AppComponents import User


class MainMenu(tk.Menu):
    def __init__(self, parent_frame, controller, current_directory, current_company, icon):
        tk.Menu.__init__(self, parent_frame)
        self.controller = controller
        self.menu_controller = MainMenuController(current_directory, current_company)
        self.current_directory = current_directory
        self.current_company = current_company

        self.icon = icon
        self.show_file_menu()

        # Display the menu
        self.controller.config(menu=self)

    def show_file_menu(self):
        # Add file menu, this is the header and if you click it, it drops down to the labels
        file_menu = tk.Menu(self, tearoff=False)
        self.add_cascade(label="File", menu=file_menu)

        # If user wants to change directory, this will open a new window
        file_menu.add_command(label="Change Directory", command=self.show_change_directory_gui)

        # For testing purposes, want to see if the user settings save
        file_menu.add_command(label="Test-Print User Settings",
                              command=self.menu_controller.testing_print_user_settings)

        # If user wants to quit the program entirely
        file_menu.add_command(label="Quit!", command=self.controller.close_application)

    def show_change_directory_gui(self):
        # Initialize ChangeDirectoryGUI if user wants to open that window
        change_directory_dialog = ChangeDirectoryGUI.ChangeDirectoryGUI(menu_controller=self.menu_controller,
                                                                        window_title="Change Directory",
                                                                        window_width=700, window_length=150,
                                                                        icon_path=self.icon)

    def get_controller(self):
        return self.menu_controller
