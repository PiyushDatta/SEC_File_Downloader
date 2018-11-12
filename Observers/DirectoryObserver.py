from Observers import ObserverInterface
from AppGUI import MainGUI


class CurrentDirectoryObserver(ObserverInterface):
    """
    Implement the Observer updating interface to keep its state
    consistent with the subject's.
    Store state that should stay consistent with the subject's.
    """

    def __init__(self):
        super(CurrentDirectoryObserver, self).__init__()
        self._directory_state = MainGUI.MainGUIApp.get_current_user_directory()

    def update(self, new_dir):
        self._directory_state = new_dir
        MainGUI.MainGUIApp.set_current_user_directory(new_dir)
