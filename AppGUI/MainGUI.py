#!/usr/bin/env python
import os
import pickle
import sys

import tkinter as tk
from tkinter import ttk, Tk, Menu, Label, StringVar, OptionMenu, Entry, Button, messagebox, Canvas, HORIZONTAL, Text, \
    END
from tkinter.ttk import Separator

from bs4 import BeautifulSoup
from urllib.request import urlopen, Request

from AppGUI.MainGUIActions import MainGUIActions
from AppGUI.PopUpWindow import ChangeDirectoryGUI, DownloadFileTypeDetailsGUI
from AppGUI.TopLayerPanel import TopPanel
from AppGUI.FileDownloadPanel import FileDownloadsPanel
from AppGUI.MainMenuPanel import MainMenuBar
from AppComponents.User import CurrentUser, Company
from AppComponents import SECCompanyList
from AppComponents.SECFileDownloader import FileDownloader
from Observers import DirectoryObserver, FileTypeDetailsObserver
from AppGUI.AutoCompleteDropdownList import AutocompleteEntry


# Remember that this window runs in the ./AppGui folder, so any assets should be in there Naming convention by
# Google: module_name, package_name, ClassName, method_name, ExceptionName, function_name,
# GLOBAL_CONSTANT_NAME, global_var_name, instance_var_name, function_parameter_name, local_var_name.

# raise ConnectionError(e, request=request)
class MainGUIApp(tk.Tk):
    def __init__(self, window_title, window_width, window_length):

        # Window settings
        tk.Tk.__init__(self)
        self.title(window_title)
        self.icon = os.getcwd() + '\\SEFD_logo_icon.ico'
        self.iconbitmap(self.icon)

        # get screen width and height
        ws = self.winfo_screenwidth()
        hs = self.winfo_screenheight()

        # calculate position x, y
        x = (ws / 2) - (window_width / 2)
        y = (hs / 2) - (window_length / 2)
        self.geometry('%dx%d+%d+%d' % (window_width, window_length, x, y))

        # Initialize existing or new user
        # super().__init__()
        self.current_user = CurrentUser()

        # Load up saved data from pickle file, this will always be saved to SEC_file_downloader folder
        self._pickle_file = os.path.abspath(os.path.join(os.getcwd(), os.pardir)) + "\\CurrentUser.svc"
        self.load_user_details()

        # Set current directory as user's last directory, if None then directory will be none
        self.current_directory = os.path.abspath(os.path.join(os.getcwd(), os.pardir))
        self.current_directory = self.current_user.get_current_directory()

        # Set chosen company to display to None until initialized
        self.current_company = None
        self.current_company = self.current_user.get_chosen_company()

        # SEC File Downloader object
        self.sec_file_downloader = FileDownloader(self.current_directory, self.current_company)

        self.file_type_details_gui = None
        self.file_type_details = None

        # Set change directory window/dialog to None until initialized
        self.change_directory_dialog = None

        container = tk.Frame(self)
        container.grid(sticky="nsew")
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        # Add all our frames
        self.frames = {}
        for F in (TopPanel, FileDownloadsPanel):
            page_name = F.__name__
            print(page_name)
            # Top Panel
            if page_name == "AppGUI.TopLayerPanel.TopPanel":
                self.top_panel = F.TopPanel(parent_frame=container, controller=self,
                                            current_directory=self.current_directory,
                                            current_company=self.current_company)
                self.frames[page_name] = self.top_panel

            # Downloads Panel
            if page_name == "AppGUI.FileDownloadPanel.FileDownloadsPanel":
                self.downloads_panel = F.DownloadPanel(parent_frame=container, controller=self,
                                                       current_directory=self.current_directory,
                                                       current_company=self.current_company,
                                                       icon=self.icon)
                self.frames[page_name] = self.downloads_panel

        # Add all our menus
        self.menus = {}
        for M in (MainMenuBar,):
            page_name = M.__name__
            self.main_menu = M.MainMenu(parent_frame=container, controller=self,
                                        current_directory=self.current_directory, current_company=self.current_company,
                                        icon=self.icon)
            self.menus[page_name] = self.main_menu

        # Initiate our controllers and observers and set them to each other
        self.main_gui_actions = MainGUIActions(self.current_directory,
                                               self.current_company,
                                               self.top_panel.get_controller(),
                                               self.downloads_panel.get_controller(),
                                               self.main_menu.get_controller())
        self.main_gui_actions.set_observer_targets()
        self.main_gui_actions.set_all_controller_observers()

        # Show TopPanel
        self.show_top_panel_frame()

        # Show DownloadsPanel (consists of download buttons)
        self.show_downloads_panel_frame()

        # Show Menu bar
        self.show_menu("AppGUI.MainMenuPanel.MainMenuBar")

        # Display company information if current company is not None
        # if self.current_company is not None:
        #     self.company_information()

        # Closing app
        self.protocol("WM_DELETE_WINDOW", self.close_application)

    def show_top_panel_frame(self):
        print("Showing: " + "AppGUI.TopLayerPanel.TopPanel")
        top_panel_frame = self.frames["AppGUI.TopLayerPanel.TopPanel"]
        top_panel_frame.grid_remove()
        top_panel_frame.grid(row=1, column=1)

    def show_downloads_panel_frame(self):
        print("Showing: " + "AppGUI.FileDownloadPanel.FileDownloadsPanel")
        downloads_panel_frame = self.frames["AppGUI.FileDownloadPanel.FileDownloadsPanel"]
        downloads_panel_frame.grid_remove()
        downloads_panel_frame.grid(row=2, column=1, sticky="w")

    def show_menu(self, page_name):
        print("Showing: " + page_name)
        self.config(menu="")
        menu = self.menus[page_name]
        self.config(menu=menu)

    # def company_information(self):
    #
    #     # Enter button to select the company
    #     # Enter button to select the company
    #     search_company_button = Button(self, text="Download 10k",
    #                                    command=self.show_file_type_details_gui,
    #                                    height=1,
    #                                    width=15)
    #     search_company_button.grid(row=6, sticky='w', padx=(10, 9), )

    #
    # ten_k_annual_reports_downloader = Button(self, text="Search",
    #                                command=lambda: sec_file_downloader.down
    #                                height=1,
    #                                width=15)

    # def show_file_type_details_gui(self):
    #
    #     self.file_type_details_gui = DownloadFileTypeDetailsGUI.FileTypeDetailsGUI(
    #         self,
    #         directory_observer=self.directory_observer,
    #         window_title="File Type Details",
    #         window_width=550, window_length=150,
    #         icon_path=self.icon)

    # def download_file_type(self, prior_to_date, file_type, file_count):
    #     # Initialize our SEC EDGAR file downloader
    #     self.sec_file_downloader.get_company_file_type(self.current_company,
    #                                                    "320193",
    #                                                    file_type,
    #                                                    prior_to_date,
    #                                                    count=file_count)
    #     # self.file_type_details_gui.close_application()
    #     # self.confirmation_of_download()

    def confirmation_of_download(self):
        T = Text(self, height=2, width=30)
        T.pack()
        T.insert(END, "Just a text Widget\nin two lines\n")

    def show_change_directory_gui(self):
        # Initialize ChangeDirectoryGUI if user wants to open that window
        self.change_directory_dialog = ChangeDirectoryGUI.ChangeDirectoryGUI(directory_observer=self.directory_observer,
                                                                             window_title="Change Directory",
                                                                             window_width=400, window_length=250,
                                                                             icon_path=self.icon)

    def close_application(self):
        if messagebox.askokcancel("Quit", "Do you want to quit?"):
            print("Saving and closing application.")
            self.save_user_details()
            return self.destroy()

    def load_user_details(self):
        if os.path.isfile(self._pickle_file) is True:
            with open(self._pickle_file, 'rb') as f:
                self.current_user = pickle.load(f)

        print("Loaded user settings")

    def save_user_details(self):
        if "AppGUI.MainMenuPanel.MainMenuBar" in self.menus:
            self.current_user.set_current_directory(
                self.menus["AppGUI.MainMenuPanel.MainMenuBar"].get_controller().get_current_directory())
            self.current_user.set_chosen_company(
                self.menus["AppGUI.MainMenuPanel.MainMenuBar"].get_controller().get_current_company())

        elif "AppGUI.TopLayerPanel.TopPanel" in self.frames:
            self.current_user.set_current_directory(
                self.frames["AppGUI.TopLayerPanel.TopPanel"].get_controller().get_current_directory())
            self.current_user.set_chosen_company(
                self.frames["AppGUI.TopLayerPanel.TopPanel"].get_controller().get_current_company())
        else:
            self.current_user.set_current_directory(self.current_directory)
            self.current_user.set_chosen_company(self.current_company)

        with open(self._pickle_file, 'wb') as f:
            pickle.dump(self.current_user, f)

        print("Saved user settings")


def main():
    main_window = MainGUIApp("SEC Edgar File Downloader", 1000, 600)
    main_window.mainloop()


if __name__ == '__main__':
    main()
