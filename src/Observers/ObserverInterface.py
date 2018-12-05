import abc


class Observer(metaclass=abc.ABCMeta):
    """
    Define an updating interface for objects that should be notified of
    changes in a subject.
    """

    @abc.abstractmethod
    def set_controllers(self, targets):
        pass

    @abc.abstractmethod
    def update(self, new_dir):
        pass
