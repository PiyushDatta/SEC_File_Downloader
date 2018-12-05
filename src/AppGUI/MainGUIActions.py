from src.Observers.CompanyObserver import CurrentCompanyObserver
from src.Observers.DirectoryObserver import CurrentDirectoryObserver


class MainGUIActions:

    def __init__(self, current_directory, current_company, top_panel_controller, downloads_panel_controller,
                 main_menu_controller):
        # Set up controllers
        self._top_panel_controller = top_panel_controller
        self._downloads_panel_controller = downloads_panel_controller
        self._main_menu_controller = main_menu_controller
        self.directory_observer = CurrentDirectoryObserver()
        self.company_observer = CurrentCompanyObserver()

    def set_observer_targets(self):
        controllers_with_curr_dir = [self._top_panel_controller, self._downloads_panel_controller,
                                     self._main_menu_controller]
        controllers_with_curr_comp = [self._top_panel_controller, self._downloads_panel_controller,
                                      self._main_menu_controller]

        self.directory_observer.set_controllers(controllers_with_curr_dir)
        self.company_observer.set_controllers(controllers_with_curr_comp)

    def set_all_controller_observers(self):
        self.set_top_panel_controller_observers()
        self.set_downloads_panel_controller_observer()
        self.set_main_menu_controller_observer()

    def set_top_panel_controller_observers(self):
        self._top_panel_controller.set_directory_observer(self.directory_observer)
        self._top_panel_controller.set_company_observer(self.company_observer)

    def set_downloads_panel_controller_observer(self):
        self._downloads_panel_controller.set_directory_observer(self.directory_observer)
        self._downloads_panel_controller.set_company_observer(self.company_observer)

    def set_main_menu_controller_observer(self):
        self._main_menu_controller.set_directory_observer(self.directory_observer)
        self._main_menu_controller.set_company_observer(self.company_observer)
