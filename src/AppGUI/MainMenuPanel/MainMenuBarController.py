import os
import pickle

from src.AppComponents.User import CurrentUser


class MainMenuController:
    def __init__(self, curr_dir, curr_comp):
        self._current_directory = curr_dir
        self._current_company = curr_comp
        self._directory_observer = None
        self._company_observer = None

    def set_directory_observer(self, dir_observer):
        self._directory_observer = dir_observer

    def set_company_observer(self, comp_observer):
        self._company_observer = comp_observer

    def set_current_directory(self, new_dir):
        self._current_directory = new_dir

    def get_current_directory(self):
        return self._current_directory

    def set_current_company(self, new_comp):
        self._current_company = new_comp

    def get_current_company(self):
        return self._current_company

    def update_current_directory(self, new_directory):
        self._current_directory = new_directory

        if self._directory_observer is not None:
            self._directory_observer.update(self._current_directory)

    def testing_print_user_settings(self):
        print(self._current_directory)
        print(self._current_company.get_chosen_company_name())

    def save_user_details(self):
        current_user = CurrentUser()
        app_gui_dir = os.path.abspath(os.path.join(os.getcwd(), os.pardir))
        pickle_file = os.path.abspath(os.path.join(app_gui_dir, os.pardir)) + "\\CurrentUser.svc"

        current_user.set_current_directory(self._current_directory)
        current_user.set_chosen_company(self._current_company)

        with open(pickle_file, 'wb') as f:
            pickle.dump(current_user, f)

        print("Saved user settings")
