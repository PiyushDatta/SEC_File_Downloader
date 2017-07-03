
"""
The SQL database to keep track of CIK keys, Company names, etc. from the SEC website.
This is the database for pdf_file_scraper.
"""

import sqlite3
import requests
# Custom made python file, name company_information
# This file is included on Github page
from company_information import Company

# Set up cursor and connection to interact with database
conn = sqlite3.connect('sec_info.db')
conn_cursor = conn.cursor()
sec_cik_url = requests.get('https://www.sec.gov/Archives/edgar/cik-lookup-data.txt', stream=True)


# conn_cursor.execute("""CREATE TABLE Companies (
#                         line_number integer,
#                         name text,
#                         cik_key integer
#                         )"""
#                     )

def update_company_db_list():
    counter = 0
    for line in sec_cik_url.iter_lines():
        curr_comp_name = str(line)
        curr_comp_cik = str(line)

        # Split the line into just the company name
        curr_comp_name = curr_comp_name.rsplit(':')[0]
        curr_comp_name = curr_comp_name.split("b", 1)[1]
        curr_comp_name = curr_comp_name[1:]

        # Split the line into just the cik number
        curr_comp_cik = curr_comp_cik.rsplit(':')[-2]

        # Create a object out of line
        curr_comp = Company(curr_comp_name, curr_comp_cik)

        # Get all rows in database
        conn_cursor.execute("SELECT * FROM company")
        all_comp = conn_cursor.fetchall()

        # Check if row corresponds with line, if not, then insert line object
        try:
            if all_comp[counter][1] == curr_comp.name and all_comp[counter][-1] == curr_comp.cik \
                    and all_comp[counter][0] == counter:
                counter += 1
            else:
                counter += 1
                insert_company(counter, curr_comp)

        except IndexError:
            counter += 1
            insert_company(counter, curr_comp)

        print(counter)

    print("Done updating!")


def insert_company(counter, comp):
    """

    :param counter: Integer
    :param comp: Company
    :return: None
    """
    with conn:
        conn_cursor.execute("INSERT INTO company VALUES "
                            "(:line_number, :name, :cik_key)",
                            {'line_number': counter,
                             'name': comp.name,
                             'cik_key': comp.cik
                             })


def get_company_by_name(comp_name):
    """

    :param comp_name:
    :return: String
    """
    conn_cursor.execute("SELECT * FROM company WHERE name=:name",
                        {'name': comp_name}
                        )
    return conn_cursor.fetchall()


def get_company_by_cik_key(comp_cik_key):
    """

    :param comp_cik_key: String
    :return: String
    """
    conn_cursor.execute("SELECT * FROM company WHERE cik_key=:cik_key",
                        {'cik_key': comp_cik_key}
                        )
    return conn_cursor.fetchall()


def delete_all_sql_data():
    """
    WARNING, do not use, unless you are sure you want to
    delete all the data in the current sql database.
    Deletes all rows in companies table
    :return: None
    """
    conn_cursor.execute("DELETE FROM company")
    conn.commit()


def remove_company(comp):
    with conn:
        conn_cursor.execute("DELETE from company WHERE "
                            "name = :name AND "
                            "cik_key = :cik_key",
                            {'name': comp.name,
                             'cik_key': comp.cik
                             })


if __name__ == '__main__':
    update_company_db_list()
    # delete_all_sql_data()
    conn.close()
