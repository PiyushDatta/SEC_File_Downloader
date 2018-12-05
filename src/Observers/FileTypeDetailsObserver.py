from src.Observers import ObserverInterface


class FileDetailsObserver(ObserverInterface.Observer):
    """
    Implement the Observer updating interface to keep its state
    consistent with the subject's.
    Store state that should stay consistent with the subject's.
    """

    def __init__(self):
        super(FileDetailsObserver, self).__init__()
        self._file_details_state = None
        self._controllers = None

    def set_controllers(self, targets):
        self._controllers = targets

    def update(self, new_details):
        self._file_details_state = new_details

    def get_file_details(self):
        return self._file_details_state
