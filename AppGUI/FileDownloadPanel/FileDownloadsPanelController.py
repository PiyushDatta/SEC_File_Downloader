from AppComponents.SECFileDownloader import FileDownloader


class DownloadPanelController:
    def __init__(self, curr_dir, curr_comp):
        self._current_directory = curr_dir
        self._current_company = curr_comp

        self._directory_observer = None
        self._company_observer = None
        self._prior_to_date = None
        self._file_type = None
        self._file_count = None

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

    def set_prior_to_date(self, prior_to_date):
        self._prior_to_date = prior_to_date

    def set_file_type(self, file_type):
        self._file_type = file_type

    def set_file_count(self, file_count):
        self._file_count = file_count

    def download_files(self, prior_to_date, file_type, file_count):
        # SEC File Downloader object
        sec_file_downloader = FileDownloader(self._current_directory, self._current_company)
        sec_file_downloader.get_company_file_type(self._current_company.get_chosen_company_name(),
                                                  self._current_company.get_chosen_company_cik_key(),
                                                  file_type,
                                                  prior_to_date,
                                                  count=file_count)
