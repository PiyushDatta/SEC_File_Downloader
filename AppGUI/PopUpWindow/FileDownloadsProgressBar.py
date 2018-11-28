import queue
import threading
import time
import sys, io
import tkinter as tk
from tkinter import Label, messagebox, HORIZONTAL, CENTER, LEFT
from tkinter.ttk import Progressbar

from AppComponents.ThreadingClient import ThreadedClient


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
        self.progress_bar_percent = None
        self.progress_bar_text = None

        self.prior_to_date = prior_to_date
        self.file_type = file_type
        self.file_count = file_count

        self.sender_queue = queue.Queue()
        self.return_queue = queue.Queue()

        self.show_progress_bar()
        self.show_progress_bar_percent()
        self.show_progress_bar_text()
        self.show_file_details()
        self.run_progress_bar()

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
        self.progress_bar.grid(row=4, column=1, sticky="w", pady=(10, 0), padx=(20, 0))
        self.progress_bar.start()

    def show_progress_bar_percent(self):
        self.progress_bar_percent = Label(self, text="0%", font=("Helvetica", 12))
        self.progress_bar_percent.grid(row=3, column=1, sticky="nsew", pady=(20, 0))

    def show_progress_bar_text(self):
        self.progress_bar_text = Label(self, text="Getting files...", font=("Helvetica", 12))
        self.progress_bar_text.grid(row=5, column=1, sticky="nsew", pady=(10, 0), padx=(5, 0))

    def run_progress_bar(self):
        # Show our progress bar
        self.progress_bar['value'] = 0
        self.progress_bar.update()

        # Set up our sender queue to send variables to downloads_panels_controller
        self.sender_queue.put(self.prior_to_date)
        self.sender_queue.put(self.file_type)
        self.sender_queue.put(self.file_count)

        # Start first thread to generate html file urls and file names
        t1 = threading.Thread(target=self.downloads_panel_controller.get_html_files_for_conversion,
                              args=(self.sender_queue, self.return_queue,))
        t1.start()
        t1.join()

        # Update again so we don't lose our progress bar
        self.progress_bar['value'] = 0
        self.progress_bar.update()

        # Get the html file urls and file names as a dict
        results = self.return_queue.get()

        # Set our progress bar max to the length of the results, so we can evenly step/progress the bar
        # by equal portions in our for loop in the next line
        self.progress_bar['maximum'] = len(results.items()) + 1

        # Loop over the key (file name) and value (url) of the dict results.
        # During the for loop, start our second thread for downloads_panel_controller and
        # also progress our progress bar by 1 each time.
        progress_percent_count = 1
        backup = sys.stdout
        for key, value in iter(results.items()):
            sys.stdout = io.StringIO()
            t2 = threading.Thread(target=self.downloads_panel_controller.download_one_file,
                                  args=(value, key,))
            t2.start()
            self.progress_bar_text['text'] = "Getting: " + sys.stdout.getvalue()
            t2.join()
            sys.stdout.close()

            sys.stdout = backup

            self.progress_bar.step(1 / len(results.items()))
            self.progress_bar_percent['text'] = "{0:.0%}".format(progress_percent_count / len(results.items()))
            self.progress_bar.update()
            progress_percent_count += 1

        # Update our progress bar with value of max to show we're done
        self.progress_bar_percent['text'] = "100%"
        self.progress_bar_text['text'] = "Almost done, please wait."
        self.progress_bar['value'] = self.progress_bar['maximum']
        self.progress_bar.update()
        self.progress_bar.stop()

        # Show our confirmation of download dialog
        self.show_download_confirmation_dialog()

    def show_download_confirmation_dialog(self):
        self.close_application()
        messagebox.showinfo(title="Download Status", message="All files downloaded!")

    # Close application
    def close_application(self):
        print("Closing FileTypeDetailsGUI application.")
        return self.destroy()
