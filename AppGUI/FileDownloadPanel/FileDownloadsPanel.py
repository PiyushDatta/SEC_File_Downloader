from AppGUI.FileDownloadPanel.FileDownloadsPanelController import DownloadPanelController
import tkinter as tk
from tkinter import Button

from AppGUI.PopUpWindow import DownloadFileTypeDetailsGUI


class DownloadPanel(tk.Frame):
    def __init__(self, parent_frame, controller, current_directory, current_company, icon):
        tk.Frame.__init__(self, parent_frame)
        self.controller = controller
        self.downloads_panel_controller = DownloadPanelController(current_directory, current_company)
        self.icon = icon
        self.file_type_details_gui = None
        self.search_company_button = None
        row_count = 6
        self.show_file_type_download_button("10-Q", row_count)
        self.show_file_type_download_button("10-K", row_count + 1)
        self.show_file_type_download_button("8-K", row_count + 2)
        self.show_file_type_download_button("DEF", row_count + 3)
        self.show_file_type_download_button("any file type", row_count + 4)

    def show_file_type_download_button(self, file_type, row_num):
        self.search_company_button = Button(self, text="Download " + file_type,
                                            command=lambda: self.show_file_type_details_gui(file_type),
                                            height=1,
                                            width=15)
        self.search_company_button.config(height=3, width=28)
        self.search_company_button.grid(row=row_num, sticky='w', padx=(12, 9), pady=(15, 10))

    def show_file_type_details_gui(self, file_type):
        if file_type == "any file type":
            file_type = None

        self.file_type_details_gui = DownloadFileTypeDetailsGUI.FileTypeDetailsGUI(
            downloads_panels_controller=self.downloads_panel_controller,
            window_title="File Type Details",
            window_width=550, window_length=150,
            icon_path=self.icon,
            chosen_file_type=file_type)

    def get_controller(self):
        return self.downloads_panel_controller
