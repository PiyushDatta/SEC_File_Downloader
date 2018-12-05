import os
import sqlite3

from AppComponents import SEC_sql_database


class CompanyList:

    def __init__(self):
        self._company_list = {}
        self._parent_dir = os.path.abspath(os.path.join(os.getcwd(), os.pardir))

    def update_list_from_db(self):
        # Get our db
        conn = sqlite3.connect(self._parent_dir + '\\sec_info.db')

        # Setup our row factory
        conn.row_factory = sqlite3.Row
        c = conn.cursor()
        c.execute('select * from companies')

        # Copy all elements as row objects into our dict
        self._company_list = c.fetchall()

    def set_company_dict(self, comp_list):
        self._company_list = comp_list

    def get_company_dict(self):
        return self._company_list

    def get_formatted_company_list(self):
        formatted_list = []
        for row in self._company_list:
            formatted_list.append(str(row[1]) + " - " + str(row[2]))

        return formatted_list

    def get_company_name_list(self):
        formatted_list = []
        for row in self._company_list:
            formatted_list.append(str(row[1]))

        return formatted_list

