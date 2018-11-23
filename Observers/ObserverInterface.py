import abc


class Observer(metaclass=abc.ABCMeta):
    """
    Define an updating interface for objects that should be notified of
    changes in a subject.
    """

    def __init__(self):
        self._subject = None

    @abc.abstractmethod
    def update(self, new_dir):
        pass
