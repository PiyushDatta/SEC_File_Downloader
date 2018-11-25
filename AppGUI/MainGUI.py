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
from AppGUI.MainMenuPanel import MainMenuBar
from AppComponents.User import CurrentUser, Company
from AppComponents import SECCompanyList
from AppComponents.SECFileDownloader import FileDownloader
from Observers import DirectoryObserver, FileTypeDetailsObserver
from AppGUI.AutoCompleteDropdownList import AutocompleteEntry


# Remember that this window runs in the ./AppGui folder, so any assets should be in there Naming convention by
# Google: module_name, package_name, ClassName, method_name, ExceptionName, function_name,
# GLOBAL_CONSTANT_NAME, global_var_name, instance_var_name, function_parameter_name, local_var_name.

#raise ConnectionError(e, request=request)
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

        self.frames = {}
        for F in (TopPanel,):
            page_name = F.__name__
            self.top_panel = F.TopPanel(parent_frame=container, controller=self, current_directory=self.current_directory,  current_company=self.current_company)
            self.frames[page_name] = self.top_panel
            # self.top_panel.grid(row=0, column=0, sticky="nsew")

        self.menus = {}
        for M in (MainMenuBar,):
            page_name = M.__name__
            self.main_menu = M.MainMenu(parent_frame=container, controller=self, current_directory=self.current_directory,  current_company=self.current_company, icon=self.icon)
            self.menus[page_name] = self.main_menu
        ################################################################################################################
        ################################################################################################################
        # self.top_panel = TopPanel.TopPanel(self, self.current_directory, self.current_company)
        self.main_gui_actions = MainGUIActions(self.current_directory,
                                               self.current_company,
                                               self.top_panel.get_controller(),
                                               self.main_menu.get_controller())
        self.main_gui_actions.set_observer_targets()
        self.main_gui_actions.set_all_controller_observers()
        ################################################################################################################
        ################################################################################################################
        self.show_frame("AppGUI.TopLayerPanel.TopPanel")
        self.show_menu("AppGUI.MainMenuPanel.MainMenuBar")
        # Make an observer a set
        # self._observers = set()

        # Add DirectoryObserver
        # self.directory_observer = DirectoryObserver.CurrentDirectoryObserver()
        # self.attach_observer(self.directory_observer)

        # Add FileTypeDetailsObserver
        # self.file_details_observer = FileTypeDetailsObserver.FileDetailsObserver()
        # self.attach_observer(self.file_details_observer)

        # Update DirectoryObserver, key word is name of observer object for this class
        # self._notify_observer("directory_observer")

        # Set main menu bar and home page
        # self.home_page()
        # self.main_menu_bar()

        # Display company information if current company is not None
        if self.current_company is not None:
            self.company_information()

        # Closing app
        self.protocol("WM_DELETE_WINDOW", self.close_application)

    def show_frame(self, page_name):
        print("Showing: " + page_name)
        for frame in self.frames.values():
            frame.grid_remove()
        frame = self.frames[page_name]
        frame.grid()

    def show_menu(self, page_name):
        print("Showing: " + page_name)
        self.config(menu="")
        menu = self.menus[page_name]
        self.config(menu=menu)

    def main_menu_bar(self):
        menu_bar = Menu(self)

        # Add file menu, this is the header and if you click it, it drops down to the labels
        file_menu = Menu(menu_bar, tearoff=False)
        menu_bar.add_cascade(label="File", menu=file_menu)

        # If user wants to change directory, this will open a new window
        file_menu.add_command(label="Change Directory", command=self.show_change_directory_gui)

        # For testing purposes, want to see if the user settings save
        file_menu.add_command(label="Test-Print User Settings", command=self.testing_print_user_settings)

        # If user wants to quit the program entirely
        file_menu.add_command(label="Quit!", command=self.close_application)

        # Display the menu
        self.config(menu=menu_bar)

    def home_page(self):
        # Have a text for current directory, pad y by 20, and set anchor to w (west)
        if self.current_directory is None:
            current_directory_text = Label(self,
                                           text="Current Directory:" + '                               '
                                                + "No directory assigned",
                                           font=("Helvetica", 12), anchor='w', pady=20)
        else:
            current_directory_text = Label(self,
                                           text="Current Directory:" + '                               '
                                                + self.current_directory,
                                           font=("Helvetica", 12), anchor='w', pady=20)
        current_directory_text.grid(row=0, sticky="w")

        # Search SEC company listings
        self.search_company_text = Label(self, text="Search SEC company directory: ", font=("Helvetica", 12))
        self.search_company_text.grid(row=1, sticky="w")

        # Drop down for searching SEC company listings (might add later)
        # =============================================================
        # db_downloader = SECCompanyList.CompanyList()
        # db_downloader.update_list_from_db()
        # SEC_COMPANY_LISTINGS = db_downloader.get_company_name_list()
        # search_company_dropdown = AutocompleteEntry(SEC_COMPANY_LISTINGS, self, width=100)
        # =============================================================

        # Make entry for searching companies, and make sure anything written is in caps
        inputted_text = StringVar()
        search_company_dropdown = Entry(self, width=100, textvariable=inputted_text)
        inputted_text.trace("w", lambda *_, var=inputted_text: self.autocapitalize_stringvar(var))
        search_company_dropdown.grid(row=1, padx=(250, 0))

        # Enter button to select the company
        search_company_button = Button(self, text="Search",
                                       command=lambda: self.get_company_entry_text(search_company_dropdown.get()),
                                       height=1,
                                       width=15)
        search_company_button.grid(column=2, row=1, padx=10, pady=(0, 5))

        # Horizontal line separator
        horizontal_line_sep = Separator(self, orient=HORIZONTAL)
        horizontal_line_sep.grid(row=4, columnspan=5, sticky="ew")

    def company_information(self):

        # Enter button to select the company
        # Enter button to select the company
        search_company_button = Button(self, text="Download 10k",
                                       command=self.show_file_type_details_gui,
                                       height=1,
                                       width=15)
        search_company_button.grid(row=6, sticky='w', padx=(10, 9), )

        #
        # ten_k_annual_reports_downloader = Button(self, text="Search",
        #                                command=lambda: sec_file_downloader.down
        #                                height=1,
        #                                width=15)

    def show_file_type_details_gui(self):

        self.file_type_details_gui = DownloadFileTypeDetailsGUI.FileTypeDetailsGUI(
            self,
            directory_observer=self.directory_observer,
            window_title="File Type Details",
            window_width=550, window_length=150,
            icon_path=self.icon)

    def download_file_type(self, prior_to_date, file_type, file_count):
        # Initialize our SEC EDGAR file downloader
        self.sec_file_downloader.get_company_file_type(self.current_company,
                                                       "320193",
                                                       file_type,
                                                       prior_to_date,
                                                       count=file_count)
        # self.file_type_details_gui.close_application()
        # self.confirmation_of_download()

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
        self.current_user.set_current_directory(self.current_directory)
        self.current_user.set_chosen_company(self.current_company)
        with open(self._pickle_file, 'wb') as f:
            pickle.dump(self.current_user, f)

        print("Saved user settings")

    def attach_observer(self, observer):
        observer._subject = self
        self._observers.add(observer)

    def detach_observer(self, observer):
        observer._subject = None
        self._observers.discard(observer)

    def _notify_observer(self, type_of_observer):
        for observer in self._observers:
            if type_of_observer is "directory_observer" and observer is self.directory_observer:
                observer.update(self.current_directory)

    def update_from_observer(self):
        print("Updating from observers")
        for observer in self._observers:
            # Update our current directory from DirectoryObserver
            if observer is isinstance(observer, DirectoryObserver.CurrentDirectoryObserver):
                self.current_directory = observer.get_directory()

    def get_company_entry_text(self, chosen_company_str):
        print("Chosen company: " + chosen_company_str)

        # First check to see if the given string is a ticker symbol
        # If so then len(links) would not be 0
        ticker_url = "https://www.sec.gov/cgi-bin/browse-edgar?CIK=" + str(
            chosen_company_str) + "&owner=exclude&action=getcompany"

        req = Request(ticker_url)
        html_page = urlopen(req).read()
        soup = BeautifulSoup(html_page, features="lxml")
        links = soup.find_all("span", {"class": "companyName"})

        if len(links) is 0:
            # SEC doesn't use spaces, they use the + sign in place of any spaces
            chosen_company_str.replace(" ", "+")

            # Now check if the given string is a company name, this name has to be exact to
            # how SEC writes it down. The company's legal name.
            # If len(links) is 0, that means this string is completely invalid.
            company_name_url = "https://www.sec.gov/cgi-bin/browse-edgar?company=" + str(
                chosen_company_str) + "&owner=exclude&action=getcompany"

            req = Request(company_name_url)
            html_page = urlopen(req).read()
            soup = BeautifulSoup(html_page, features="lxml")
            links = soup.find_all("span", {"class": "companyName"})

            if len(links) is 0:
                self.update_current_company(None)
                return

        # From the link, whether it be a ticker symbol or actual company legal name,
        # get the company name and cik key. Create a new company object from these 2 vars.
        company_name = str(links[0].text.split("CIK#:")[0]).strip()
        cik_key = str(links[0].text.split("CIK#:")[1]).strip().split(" ", 1)[0]
        new_company = Company.CurrentCompany(company_name, cik_key)

        print("Chosen company name: " + new_company.get_chosen_company_name())
        print("Chosen company cik key: " + new_company.get_chosen_company_cik_key())
        self.update_current_company(new_company)

    def update_current_company(self, new_company):
        if new_company is None:
            self.current_company = None
            self.sec_file_downloader.set_current_company(self.current_company)
            self.search_company_text.config(text="No company selected / Wrong company name selected")
        else:
            self.current_company = new_company
            self.sec_file_downloader.set_current_company(self.current_company)
            self.search_company_text.config(text=self.current_company.get_chosen_company_name())

    def testing_print_user_settings(self):
        print(self.current_directory)
        print(self.current_company.get_chosen_company_name())

    def autocapitalize_stringvar(self, var):
        if isinstance(var, StringVar):
            var.set(var.get().upper())


def main():
    main_window = MainGUIApp("SEC Edgar File Downloader", 1000, 600)
    # directory_observer = DirectoryObserver.CurrentDirectoryObserver()
    # main_window.attach_observer(directory_observer)
    main_window.mainloop()


if __name__ == '__main__':
    main()
