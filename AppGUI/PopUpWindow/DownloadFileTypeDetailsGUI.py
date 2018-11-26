import tkinter as tk
from tkinter import Label, StringVar, Entry, Button

from AppGUI.PopUpWindow.FileDownloadsProgressBar import DownloadsProgressBar


class FileTypeDetailsGUI(tk.Tk):
    def __init__(self, downloads_panels_controller, window_title, window_width, window_length, icon_path):
        # Window settings
        tk.Tk.__init__(self)
        self.title(window_title)

        self.iconbitmap(icon_path)

        # get screen width and height
        ws = self.winfo_screenwidth()
        hs = self.winfo_screenheight()

        # calculate position x, y
        x = (ws / 2) - (window_width / 2)
        y = (hs / 2) - (window_length / 2)
        self.geometry('%dx%d+%d+%d' % (window_width, window_length, x, y))

        self.downloads_panel_controller = downloads_panels_controller

        # Initialize current directory as none then get update from observer
        self.current_directory = None

        self.prior_to_date = None

        self.file_type = None

        self.file_count = None

        self.ret_list = None

        self.prior_to_date_widget()
        self.file_type_widget()
        self.file_count_widget()
        self.confirmation_button()

        self.protocol("WM_DELETE_WINDOW", self.close_application)

    def prior_to_date_widget(self):
        self.prior_to_date = StringVar()

        prior_to_text = Label(self, text="Enter prior to date (YYYYMMDD): ", font=("Helvetica", 12))
        prior_to_entry = Entry(self, width=30, textvariable=self.prior_to_date)

        prior_to_text.grid(row=1, sticky="w")
        prior_to_entry.grid(row=1, padx=(300, 0))

        self.prior_to_date.set("20180101")

    def file_type_widget(self):
        self.file_type = StringVar()

        file_type_text = Label(self, text="Enter file type (ex: 10-Q): ", font=("Helvetica", 12))
        file_type_entry = Entry(self, width=30, textvariable=self.file_type)

        file_type_text.grid(row=2, sticky="w")
        file_type_entry.grid(row=2, padx=(300, 0))

        self.file_type.set("10-Q")

    def file_count_widget(self):
        self.file_count = StringVar()

        file_count_text = Label(self, text="Enter number of files wanted (ex: 10): ", font=("Helvetica", 12))
        file_count_entry = Entry(self, width=30, textvariable=self.file_count)

        file_count_text.grid(row=3, sticky="w")
        file_count_entry.grid(row=3, padx=(300, 0))

        self.file_count.set("10")

    def confirmation_button(self):
        confirm_button = Button(self, text="Confirm",
                                command=self.send_to_progress_bar,
                                height=1,
                                width=15)
        confirm_button.grid(row=4, padx=10, pady=(10, 0))

    def send_to_progress_bar(self):
        self.close_application()
        DownloadsProgressBar(self.downloads_panel_controller, "Download Progress", 550, 150,
                             self.iconbitmap, self.prior_to_date.get(), self.file_type.get(), self.file_count.get())

    # Close application
    def close_application(self):
        print("Closing FileTypeDetailsGUI application.")
        return self.destroy()
