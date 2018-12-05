from tkinter import StringVar, HORIZONTAL, Label
from tkinter.ttk import Separator, Entry, Button
import tkinter as tk

from src.AppGUI.TopLayerPanel.TopPanelController import TopPanelController


class TopPanel(tk.Frame):
    def __init__(self, parent_frame, controller, current_directory, current_company):
        tk.Frame.__init__(self, parent_frame)
        self.controller = controller
        self.top_panel_controller = TopPanelController(self, current_directory, current_company)
        self.current_directory_text = None
        self.current_company_selection_text = None

        # Show everything
        self.show_current_directory()
        self.show_company_search()
        self.show_current_company_selection()

    def get_controller(self):
        return self.top_panel_controller

    def show_current_directory(self):

        # Have a text for current directory, pad y by 20, and set anchor to w (west)
        if self.top_panel_controller.get_current_directory() is None:
            self.current_directory_text = Label(self,
                                                text="Current Directory:" + '                               '
                                                     + "No directory assigned",
                                                font=("Helvetica", 12), anchor='w', pady=20)
        else:
            self.current_directory_text = Label(self,
                                                text="Current Directory:" + '                               '
                                                     + self.top_panel_controller.get_current_directory(),
                                                font=("Helvetica", 12), anchor='w', pady=20)

        self.current_directory_text.grid(row=0, sticky="w")

    def show_company_search(self):

        # Search SEC company listings
        search_company_text = Label(self, text="Search SEC company directory: ", font=("Helvetica", 12))
        search_company_text.grid(row=1, sticky="w")

        # Drop down for searching SEC company listings (might add later)
        # =============================================================
        # db_downloader = SECCompanyList.CompanyList()
        # db_downloader.update_list_from_db()
        # SEC_COMPANY_LISTINGS = db_downloader.get_company_name_list()
        # search_company_dropdown = AutocompleteEntry(SEC_COMPANY_LISTINGS, self, width=100)
        # =============================================================

        # Make entry for searching companies, and make sure anything written is capitalized
        inputted_text = StringVar()
        search_company_dropdown = Entry(self, width=100, textvariable=inputted_text)
        inputted_text.trace("w", lambda *_, var=inputted_text: auto_capitalize_string_var(var))
        search_company_dropdown.grid(row=1, padx=(250, 0))

        # Enter button to select the company, calls TopPanelController class to search for this company
        search_company_button = Button(self, text="Search",
                                       command=lambda: self.top_panel_controller.search_for_selected_company(
                                           search_company_dropdown.get()))
        search_company_button.config(width=15)
        search_company_button.grid(column=2, row=1, padx=10, pady=(0, 5))

        # Horizontal line separator, gui design purposes
        horizontal_line_sep = Separator(self, orient=HORIZONTAL)
        horizontal_line_sep.grid(row=4, columnspan=5, pady=(5, 0), sticky="ew")

    def show_current_company_selection(self):
        # Display current company selection
        if self.top_panel_controller.get_current_company() is None:
            self.current_company_selection_text = Label(self,
                                                        text="Not a valid SEC ticker symbol or company name",
                                                        font=("Helvetica", 12),
                                                        justify='center')
        else:
            self.current_company_selection_text = Label(self,
                                                        text=self.top_panel_controller.get_current_company().get_chosen_company_name(),
                                                        font=("Helvetica", 12),
                                                        justify='center')

        self.current_company_selection_text.grid(row=5, padx=(200, 0), pady=10)

    def restart_panel(self):
        self.refresh_panel()
        self.controller.show_top_panel_frame()

    def refresh_panel(self):

        # Refresh/update company name
        if self.top_panel_controller.get_current_company() is None:
            self.current_company_selection_text.config(text="Not a valid SEC ticker symbol or company name")
        else:
            comp_name = self.top_panel_controller.get_current_company().get_chosen_company_name()
            self.current_company_selection_text.config(text=comp_name)

        # Refresh/update current directory name
        curr_dir = "Current Directory:" + '                               '
        if self.top_panel_controller.get_current_directory() is None:

            self.current_directory_text.config(text=curr_dir + "No directory assigned")
        else:
            self.current_directory_text.config(text=curr_dir + self.top_panel_controller.get_current_directory())


def auto_capitalize_string_var(var):
    if isinstance(var, StringVar):
        var.set(var.get().upper())
