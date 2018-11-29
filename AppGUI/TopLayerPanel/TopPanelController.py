from urllib.request import Request, urlopen

from bs4 import BeautifulSoup

from AppComponents import Company
from Observers import DirectoryObserver


class TopPanelController:
    def __init__(self, panel, curr_dir, curr_comp):
        self._panel = panel
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
        self._panel.restart_panel()

    def get_current_directory(self):
        return self._current_directory

    def set_current_company(self, new_comp):
        self._current_company = new_comp
        self._panel.restart_panel()

    def get_current_company(self):
        return self._current_company

    def update_current_company(self, new_company):
        self._current_company = new_company
        self._panel.restart_panel()

        if self._company_observer is not None:
            self._company_observer.update(self._current_company)

    def search_for_selected_company(self, chosen_company_str):
        print("Chosen company: " + chosen_company_str)

        # First check to see if the given string is a ticker symbol
        # If so then len(links) would not be 0
        ticker_url = "https://www.sec.gov/cgi-bin/browse-edgar?CIK=" + str(
            chosen_company_str) + "&owner=exclude&action=getcompany"

        req = Request(ticker_url)
        html_page = urlopen(req).read()
        soup = BeautifulSoup(html_page, features="lxml")
        links = soup.find_all("span", {"class": "companyName"})

        if len(links) is 0:
            # SEC doesn't use spaces, they use the + sign in place of any spaces
            chosen_company_str.replace(" ", "+")

            # Now check if the given string is a company name, this name has to be exact to
            # how SEC writes it down. The company's legal name.
            # If len(links) is 0, that means this string is completely invalid.
            company_name_url = "https://www.sec.gov/cgi-bin/browse-edgar?company=" + str(
                chosen_company_str) + "&owner=exclude&action=getcompany"

            req = Request(company_name_url)
            html_page = urlopen(req).read()
            soup = BeautifulSoup(html_page, features="lxml")
            links = soup.find_all("span", {"class": "companyName"})

            if len(links) is 0:
                self.update_current_company(new_company=None)
                return

        # From the link, whether it be a ticker symbol or actual company legal name,
        # get the company name and cik key. Create a new company object from these 2 vars.
        company_name = str(links[0].text.split("CIK#:")[0]).strip()
        cik_key = str(links[0].text.split("CIK#:")[1]).strip().split(" ", 1)[0]
        new_company = Company.CurrentCompany(company_name, cik_key)

        print("Chosen company name: " + new_company.get_chosen_company_name())
        print("Chosen company cik key: " + new_company.get_chosen_company_cik_key())
        self.update_current_company(new_company=new_company)
