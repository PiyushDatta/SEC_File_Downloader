import os


class CurrentCompany:
    """
    Current company and their settings
    """

    def __init__(self, curr_company_name, cik_key):
        self._company_name = curr_company_name
        self._company_cik_key = cik_key

    def set_company_name(self, new_company):
        self._company_name = new_company

    def get_chosen_company_name(self):
        return self._company_name

    def set_company_cik_key(self, new_cik_key):
        self._company_cik_key = new_cik_key

    def get_chosen_company_cik_key(self):
        return self._company_cik_key
