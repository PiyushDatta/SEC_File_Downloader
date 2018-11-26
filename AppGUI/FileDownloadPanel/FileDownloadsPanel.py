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
        self.show_ten_k_download_button()

    def show_ten_k_download_button(self):
        self.search_company_button = Button(self, text="Download 10k",
                                            command=self.show_file_type_details_gui,
                                            height=1,
                                            width=15)
        self.search_company_button.grid(row=6, sticky='w', padx=(10, 9), )

    def show_file_type_details_gui(self):
        self.file_type_details_gui = DownloadFileTypeDetailsGUI.FileTypeDetailsGUI(
            downloads_panels_controller=self.downloads_panel_controller,
            window_title="File Type Details",
            window_width=550, window_length=150,
            icon_path=self.icon)

    def get_controller(self):
        return self.downloads_panel_controller
