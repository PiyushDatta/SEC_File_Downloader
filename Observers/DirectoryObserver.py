from Observers import ObserverInterface
from AppGUI import MainGUI


class CurrentDirectoryObserver(ObserverInterface.Observer):
    """
    Implement the Observer updating interface to keep its state
    consistent with the subject's.
    Store state that should stay consistent with the subject's.
    """

    def __init__(self):
        super(CurrentDirectoryObserver, self).__init__()

    def update(self, new_dir):
        self._directory_state = new_dir

    def get_directory(self):
        return self._directory_state
