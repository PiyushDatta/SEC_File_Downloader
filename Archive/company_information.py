
"""
Class to maintain the information for a company.
Mainly used for sqllite3 database
"""


class Company:
    """
    Information about a certain company
    """

    def __init__(self, comp_name, comp_cik_key):
        """

        :param comp_name: String
        :param comp_cik_key: String
        """
        self.name = comp_name
        self.cik = int(comp_cik_key)

    def __repr__(self):
        return "Company('{}', '{})".format(self.name, self.cik)
