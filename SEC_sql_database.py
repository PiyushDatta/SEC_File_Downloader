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
our_cik_txt = 'CIK_List.txt'


def create_table():
    conn_cursor.execute("""CREATE TABLE IF NOT EXISTS companies (
                            line_number INTEGER,
                            name TEXT,
                            cik_key INTEGER
                            )"""
                        )


def input_company_db_list():
    """
    Input all the companies from either a text file or the SEC url into
    the database. Each input includes line number, company name, and company cik key

    :return: None
    """
    counter = 0
    batch = list()
    # Number of companies to dump into db at once
    batch_size = 2000

    # =================
    # If using txt file
    # =================
    # with open(our_cik_txt) as SEC_listings:
    #     for line in SEC_listings:
    # curr_comp_name = str(line.rsplit(':')[0])
    # curr_comp_cik = str(line.rsplit(':')[-2])
    # =================
    for line in sec_cik_url.iter_lines():
        curr_comp_name = str(line).rsplit(':')[0][2:]
        curr_comp_cik = str(line).rsplit(':')[-2]
        counter += 1
        print(counter, curr_comp_name, curr_comp_cik)
        # insert_company(counter, curr_comp)

        # Create object of the line
        batch.append((counter, curr_comp_name, curr_comp_cik))
        # Insert company is a self-made method, listed below
        if len(batch) == batch_size:
            insert_multi_comps(batch)
            batch = list()

    # something may be still pending
    if batch:
        insert_multi_comps(batch)

    print("==== Done uploading! ====")


def insert_multi_comps(comps):
    """

    :param comps: List[Integer, String, String]
    :return: None
    """
    with conn:
        conn_cursor.executemany("INSERT INTO companies VALUES (?, ?, ?)", comps)


def insert_company(counter, comp):
    """

    :param counter: Integer
    :param comp: Company
    :return: None
    """
    with conn:
        conn_cursor.execute("INSERT INTO companies VALUES "
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
    conn_cursor.execute("SELECT * FROM companies WHERE name=:name",
                        {'name': comp_name}
                        )
    return conn_cursor.fetchall()


def get_company_by_cik_key(comp_cik_key):
    """

    :param comp_cik_key: String
    :return: String
    """
    conn_cursor.execute("SELECT * FROM companies WHERE "
                        "cik_key=:cik_key",
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
    conn_cursor.execute("DELETE FROM companies")
    conn.commit()


def remove_company(comp):
    with conn:
        conn_cursor.execute("DELETE from companies WHERE "
                            "name = :name AND "
                            "cik_key = :cik_key",
                            {'name': comp.name,
                             'cik_key': comp.cik
                             })


if __name__ == '__main__':
    # create_table()
    # input_company_db_list()
    # delete_all_sql_data()
    conn.close()
