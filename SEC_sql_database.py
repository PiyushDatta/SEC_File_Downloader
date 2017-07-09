"""
The SQL database to keep track of CIK keys, Company names, etc. from the SEC website.
This is the database for pdf_file_scraper.
"""

import sqlite3
import requests
import csv
import pandas.io.sql as sql
import pandas as pd
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

    print("==== Done inputting companies! ====")


def update_company_db_list():
    """
    In case data gets missed, and we need to add particular data in.
    Will update this after.

    :return: None
    """

    # Line 4348-4351 don't translate, so we add them here
    counter = 1
    for line in sec_cik_url.iter_lines():
        counter += 1
        if 4347 < counter <= 4351:
            curr_comp_name = str(line).rsplit(':')[0][2:]
            conn_cursor.execute("UPDATE companies SET name = :name WHERE line_number = :line_number",
                                {'line_number': counter,
                                 'name': curr_comp_name,
                                 })
            conn.commit()

        if counter > 4351:
            break


def translate_db_to_csv_file():
    """
    Make an csv file from the data in the database

    :return: None
    """

    # Create an csv file from the data from the sql file
    table = sql.read_sql('select * from companies', conn)
    table.to_csv('sec__edgar_company_info.csv')

    # Only keep these 3 column names
    sql_csv = pd.read_csv('sec__edgar_company_info.csv')
    # Change column names, for better clarity
    sql_csv.columns = ['Del After', 'Line Number', 'Company Name', 'Company CIK Key']
    keep_col = ['Line Number', 'Company Name', 'Company CIK Key']
    new_f = sql_csv[keep_col]
    new_f.to_csv("sec__edgar_company_info.csv", index=False)


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


def get_range_of_cik_keys(range_x, range_y):
    """
    Return a list of tuples, containing company details (line number, company name, and cik key).
    The list will only contain company details in range x to range y, inclusive.

    :param range_x: Integer
    :param range_y: Integer
    :return: List[(Integer, String, Integer)]
    """
    conn_cursor.execute("SELECT * FROM companies WHERE line_number BETWEEN "
                        ":range_x AND :range_y",
                        {'range_x': range_x,
                         'range_y': range_y})

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
    # translate_db_to_csv_file()
    # update_company_db_list()
    conn.close()
