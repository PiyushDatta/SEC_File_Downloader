import os


class CurrentUser:
    """
    Current user and their settings
    """

    def __init__(self):
        self._current_directory = os.path.dirname(os.getcwd())

    def set_current_directory(self, curr_dir):
        self._current_directory = curr_dir

    def get_current_directory(self):
        return self._current_directory
