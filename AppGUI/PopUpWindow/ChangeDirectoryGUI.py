import math
import os
import sys
import tkinter as tk
from tkinter import messagebox, StringVar
from tkinter.ttk import Button, Label, Entry
from AppGUI import MainGUI
from Observers import DirectoryObserver


class ChangeDirectoryGUI(tk.Toplevel):
    def __init__(self, menu_controller, window_title, window_width, window_length, icon_path, **kw):
        # Window settings
        tk.Toplevel.__init__(self)
        self.title(window_title)

        self.iconbitmap(icon_path)

        # get screen width and height
        ws = self.winfo_screenwidth()
        hs = self.winfo_screenheight()

        # calculate position x, y
        x = (ws / 2) - (window_width / 2)
        y = (hs / 2) - (window_length / 2)
        self.geometry('%dx%d+%d+%d' % (window_width, window_length, x, y))

        self._menu_controller = menu_controller
        self._current_directory_text = None
        self._new_directory_entry = None
        self._new_directory_entry_input = StringVar()
        self._confirm_button = None

        # Show everything
        self.show_current_directory()
        self.show_new_directory_entry()
        self.show_confirm_button()

    def show_current_directory(self):
        self._current_directory_text = Label(self,
                                             text="Current directory:" + '        ' + self._menu_controller.get_current_directory(),
                                             font=("Helvetica", 12))
        self._current_directory_text.grid(row=1, pady=(10, 0), padx=(5, 0), sticky="w")

    def show_new_directory_entry(self):
        new_input_text = Label(self, text="Enter new directory: ", font=("Helvetica", 12))
        self._new_directory_entry = Entry(self, width=85, textvariable=self._new_directory_entry_input)

        new_input_text.grid(row=2, column=0, pady=(20, 0), padx=(5, 0), sticky="w")
        self._new_directory_entry.grid(row=2, column=0, pady=(20, 0), padx=(160, 0))

    def show_confirm_button(self):
        self._confirm_button = Button(self, text="Confirm",
                                      command=self.show_download_confirmation_dialog)
        self._confirm_button.config(width=20)
        self._confirm_button.grid(row=3, pady=(20, 0), padx=(20, 0), ipady=5, ipadx=5)

    def show_download_confirmation_dialog(self):
        if os.path.isdir(self._new_directory_entry_input.get()):
            self._menu_controller.update_current_directory(self._new_directory_entry_input.get())
            messagebox.showinfo(title="Confirmation", message="Current directory changed!")
            self.close_application()
        else:
            messagebox.showerror(title="Error", message="Directory chosen does not exist")

    # Close application
    def close_application(self):
        print("Closing ChangeDirectoryGUI application.")
        return self.destroy()
