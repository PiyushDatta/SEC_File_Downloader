#!/usr/bin/env python
import os
import pickle
import sys
from tkinter import Tk, Menu, Label, StringVar, OptionMenu, Entry, Button, messagebox, Canvas, HORIZONTAL, Text, END
from tkinter.ttk import Separator

import requests
from lxml import html

from AppGUI.PopUpWindow import ChangeDirectoryGUI, DownloadFileTypeDetailsGUI
from AppComponents.User import CurrentUser
from AppComponents import SECCompanyList
from AppComponents.SECFileDownloader import FileDownloader
from Observers import DirectoryObserver
from AppGUI.AutoCompleteDropdownList import AutocompleteEntry


# Remember that this window runs in the ./AppGui folder, so any assets should be in there Naming convention by
# Google: module_name, package_name, ClassName, method_name, ExceptionName, function_name,
# GLOBAL_CONSTANT_NAME, global_var_name, instance_var_name, function_parameter_name, local_var_name.
class MainGUIApp(Tk):
    def __init__(self, window_title, window_width, window_length):

        # Window settings
        Tk.__init__(self)
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
        self.current_user = CurrentUser()

        # Load up saved data from pickle file
        self._pickle_file = self.current_user.get_current_directory() + "\\CurrentUser.svc"
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

        # Make an observer a set
        self._observers = set()

        # Add DirectoryObserver
        self.directory_observer = DirectoryObserver.CurrentDirectoryObserver()
        self.attach_observer(self.directory_observer)

        # Update DirectoryObserver
        self._notify_observer()

        # Set main menu bar and home page
        self.main_menu_bar()
        self.home_page()

        # Display current company selection
        self.search_company_text = Label(self, text=self.current_company, font=("Helvetica", 12), justify='center')
        self.search_company_text.grid(row=5, padx=(30, 0), pady=10)

        # Display company information if current company is not None
        if self.current_company is not None:
            self.company_information()

        # Closing app
        self.protocol("WM_DELETE_WINDOW", self.close_application)

        # self.change_directory_dialog.closeEvent(self.update_from_observer())

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

        # Drop down for searching SEC company listings
        db_downloader = SECCompanyList.CompanyList()
        db_downloader.update_list_from_db()
        SEC_COMPANY_LISTINGS = db_downloader.get_company_name_list()

        # search_company_dropdown = AutocompleteEntry(SEC_COMPANY_LISTINGS, self, width=100)
        inputted_text = StringVar()
        search_company_dropdown = Entry(self, width=100, textvariable=inputted_text)
        inputted_text.trace("w", lambda *_, var=inputted_text: self.autocapitalize_stringvar(var))
        search_company_dropdown.grid(row=1, padx=(250, 0))

        # Enter button to select the company
        search_company_button = Button(self, text="Search",
                                       command=lambda: self.get_entry_text(search_company_dropdown.get()),
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

    def main_menu_bar(self):
        menu_bar = Menu(self)
        file_menu = Menu(menu_bar, tearoff=False)
        menu_bar.add_cascade(label="File", menu=file_menu)
        file_menu.add_command(label="Change Directory", command=self.show_change_directory_gui)
        file_menu.add_command(label="Test-Print User Settings", command=self.testing_print_user_settings)
        file_menu.add_command(label="Quit!", command=self.close_application)

        # display the menu
        self.config(menu=menu_bar)

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

    def _notify_observer(self):
        for observer in self._observers:
            observer.update(self.current_directory)

    def update_from_observer(self):
        print("Updating from observers")
        for observer in self._observers:
            # Update our current directory from DirectoryObserver
            if observer is isinstance(observer, DirectoryObserver.CurrentDirectoryObserver):
                self.current_directory = observer.get_directory()

    def get_entry_text(self, chosen_company_str):
        print("Chosen company: " + chosen_company_str)

        cik_url = "https://www.sec.gov/cgi-bin/browse-edgar?CIK=" + str(
            chosen_company_str) + "&owner=exclude&action=getcompany"

        # SEC doesn't use spaces, they use the + sign in place of any spaces
        chosen_company_str.replace(" ", "+")

        company_name_url = "https://www.sec.gov/cgi-bin/browse-edgar?company=" + str(
            chosen_company_str) + "&owner=exclude&action=getcompany"

        company_name = []

        page = requests.get(cik_url)
        tree = html.fromstring(page.content)
        company_name = tree.xpath('//span[@class="companyName"]/text()')

        if not company_name:
            page = requests.get(company_name_url)
            tree = html.fromstring(page.content)
            company_name = tree.xpath('//span[@class="companyName"]/text()')
            if not company_name:
                self.update_current_company(None)
                return

        print(company_name[0])
        self.update_current_company(company_name[0])

    def update_current_company(self, new_company):
        if new_company is None:
            self.current_company = None
            self.sec_file_downloader.set_current_company(self.current_company)
            self.search_company_text.config(text="No company selected / Wrong company name selected")
        else:
            self.current_company = new_company
            self.sec_file_downloader.set_current_company(self.current_company)
            self.search_company_text.config(text=self.current_company)

    def testing_print_user_settings(self):
        print(self.current_directory)
        print(self.current_company)

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
