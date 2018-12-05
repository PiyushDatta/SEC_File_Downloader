from src.Observers import ObserverInterface


class CurrentCompanyObserver(ObserverInterface.Observer):
    """
    Implement the Observer updating interface to keep its state
    consistent with the subject's.
    Store state that should stay consistent with the subject's.
    """

    def __init__(self):
        self._controllers = None

    def set_controllers(self, targets):
        self._controllers = targets

    def update(self, new_comp):
        for controller in self._controllers:
            controller.set_current_company(new_comp)
