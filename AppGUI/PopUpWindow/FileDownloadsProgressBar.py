import time
import tkinter as tk
from tkinter import Label, messagebox, HORIZONTAL, CENTER, LEFT
from tkinter.ttk import Progressbar


class DownloadsProgressBar(tk.Tk):
    def __init__(self, downloads_panels_controller, window_title, window_width, window_length, icon_bitmap,
                 prior_to_date, file_type, file_count):
        # Window settings
        tk.Tk.__init__(self)
        self.title(window_title)

        self.iconbitmap = icon_bitmap

        # get screen width and height
        ws = self.winfo_screenwidth()
        hs = self.winfo_screenheight()

        # calculate position x, y
        x = (ws / 2) - (window_width / 2)
        y = (hs / 2) - (window_length / 2)
        self.geometry('%dx%d+%d+%d' % (window_width, window_length, x, y))

        self.downloads_panel_controller = downloads_panels_controller

        self.progress_bar = None

        self.prior_to_date = prior_to_date
        self.file_type = file_type
        self.file_count = file_count

        self.show_file_details()
        self.show_progress_bar()
        self.run_progress_bar()

        # self.protocol("WM_DELETE_WINDOW", self.close_application)

    def show_file_details(self):
        prior_to_space = "Prior to date (YYYY/MM/DD):   "
        file_type_space = '                                    '
        prior_to_text = Label(self, text=prior_to_space + self.prior_to_date, font=("Helvetica", 12))
        file_type_text = Label(self, text="File-type:" + file_type_space + self.file_type, font=("Helvetica", 12))
        file_count_text = Label(self, text="Number of files to download:   " + self.file_count, font=("Helvetica", 12))

        prior_to_text.grid(row=0, column=1, sticky="w", padx=(20, 0))
        file_type_text.grid(row=1, column=1, sticky="w", padx=(20, 0))
        file_count_text.grid(row=2, column=1, sticky="w", padx=(20, 0))

    def show_progress_bar(self):
        self.progress_bar = Progressbar(self, orient=HORIZONTAL, length=500, mode='determinate')
        self.progress_bar.grid(row=3, column=1, sticky="w", pady=(20, 0), padx=(20, 0))

    def run_progress_bar(self):
        self.progress_bar['maximum'] = 100

        for i in range(101):
            time.sleep(0.1)
            self.progress_bar["value"] = i
            self.progress_bar.update()

        self.download_confirmation_dialog()

    def send_to_file_downloads_controller(self):
        self.downloads_panel_controller.download_files(self.prior_to_date.get(), self.file_type.get(),
                                                       self.file_count.get())
        self.close_application()

    def download_confirmation_dialog(self):
        messagebox.showinfo(title="Download Status", message="All files downloaded!")
        self.close_application()

    # Close application
    def close_application(self):
        print("Closing FileTypeDetailsGUI application.")
        return self.destroy()
