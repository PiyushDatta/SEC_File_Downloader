import os
from src.AppComponents import Company


class CurrentUser:
    """
    Current user and their settings
    """

    def __init__(self):
        self._current_directory = os.getcwd()
        self._chosen_company = Company.CurrentCompany('APPLE INC', "0000320193")

    def set_current_directory(self, curr_dir):
        self._current_directory = curr_dir

    def get_current_directory(self):
        return self._current_directory

    def set_chosen_company(self, chosen_comp):
        self._chosen_company = chosen_comp

    def get_chosen_company(self):
        return self._chosen_company
