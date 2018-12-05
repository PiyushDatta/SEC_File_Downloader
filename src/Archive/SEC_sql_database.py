"""
The SQL database to keep track of CIK keys, Company names, etc. from the SEC website.
This is the database for pdf_file_scraper.
"""
import argparse
import csv
import os
import sqlite3
import sys

import pdfkit
import pandas as pd
import pandas.io.sql as sql
import requests
from bs4 import BeautifulSoup

from lxml import html
from urllib.request import urlopen, Request
import shutil

# Custom made python file, name company_information
# This file is included on Github page

# Set up cursor and connection to interact with database
conn = sqlite3.connect('sec_info.db')
conn_cursor = conn.cursor()
sec_cik_url = requests.get('https://www.sec.gov/Archives/edgar/cik-lookup-data.txt', stream=True)
our_cik_txt = 'CIK_List.txt'

new_url = "http://rankandfiled.com/static/export/cik_ticker.csv"


def test_scraping():
    url = new_url
    r = requests.get(url, verify=False, stream=True)
    if r.status_code != 200:
        print("Failure!!")
        exit()
    else:
        r.raw.decode_content = True
        with open("cik_ticker.csv", 'wb') as f:
            shutil.copyfileobj(r.raw, f)
        print("Success")


def new_update_db():
    counter = 1
    with open('cik_ticker.csv') as fin:  # `with` statement available in 2.5+
        # csv.DictReader uses first line in file for column headings by default
        dr = csv.DictReader(fin, delimiter='|')  # comma is default delimiter
        to_db = [(i['Name'], i['Ticker'], i['CIK'], i['Exchange'], i['SIC'], i['Business'],
                  i['Incorporated'], i['IRS']) for i in dr]

    conn_cursor.executemany(
        "INSERT INTO companies (name, ticker_symbol, cik_key, exchange, sic, business, "
        "incorporated, irs) VALUES (?, ?, ?, ?, ?, ?, ?, ?);", to_db)
    conn.commit()

    # for line in sec_cik_url.iter_lines():
    #     counter += 1
    #     if 4347 < counter <= 4351:
    #         curr_comp_name = str(line).rsplit(':')[0][2:]
    #         conn_cursor.execute("UPDATE companies SET name = :name WHERE line_number = :line_number",
    #                             {'line_number': counter,
    #                              'name': curr_comp_name,
    #                              })
    #         conn.commit()
    #
    #     if counter > 4351:
    #         break


def create_table():
    conn_cursor.execute("""CREATE TABLE IF NOT EXISTS companies (
                            name TEXT,
                            ticker_symbol TEXT,
                            cik_key INTEGER,
                            exchange TEXT,
                            sic INTEGER,
                            business TEXT,
                            incorporated TEXT,
                            irs INTEGER
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
        # print(counter, curr_comp_name, curr_comp_cik)
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


def get_company_file_type(company_name, cik_key, file_type, prior_to, count=10):
    # Generate the url to crawl
    base_url = "http://www.sec.gov/cgi-bin/browse-edgar?action=getcompany&CIK=" + str(
        cik_key) + "&type=" + str(file_type) + "&dateb=" + str(prior_to) + "&owner=exclude&output=xml&count=" + str(
        count)

    print("Base url we are trying to scrape for file types: " + base_url)

    # Parent path, will direct to annual report and wkhtmltopdf config exe file
    parent_path = os.path.abspath(os.path.join(os.getcwd(), os.pardir))

    # Where the links to the htm files that need to be translated into pdf will go
    res = []

    # Get links to type of files for company
    archives_data_links = get_file_type_htm_links(base_url, "filinghref", count)

    # Get the actual htm of the type of file for the company
    for link in archives_data_links:
        res = get_file_type_htm_links(link, "a", count)

    # Translate each htm into pdf and save it to an Annual Reports folder
    for html_link in res:
        file_name = "\\" + html_link.rsplit('/', 1)[-1].rsplit('.', 1)[0] + ".pdf"
        html_to_pdf_directly(html_link, parent_path, company_name.replace(" ", ""), file_name)

    print()
    print("Printed all " + file_type + " for: " + company_name + "!")


def html_to_pdf_directly(request, parent_path, company_name, file_name):
    # Config path to wkhtmltopdf, this exe file is needed for pdfkit
    config_path = parent_path + "\\wkhtmltopdf\\bin\\wkhtmltopdf.exe"
    config = pdfkit.configuration(wkhtmltopdf=config_path)

    # Where we will save our files
    annual_reports_path = parent_path + "\\AnnualReports"
    company_path = parent_path + "\\AnnualReports\\" + company_name

    # If Annual Reports folder doesn't exist, make it
    if not os.path.exists(annual_reports_path):
        os.mkdir(annual_reports_path)
        print("Directory: ", annual_reports_path, " == Created ")
    else:
        print("Directory: ", annual_reports_path, " == Already exists")

    # If company folder under the Annual Reports folder doesn't exist, make it
    if not os.path.exists(company_path):
        os.mkdir(company_path)
        print("Directory: ", company_path, " == Created ")
    else:
        print("Directory: ", company_path, " == Already exists")

    print("Path of file we are converting: " + company_path + file_name)

    # Get the url link to the file type and convert it into pdf
    pdfkit.from_url(request, company_path + file_name, configuration=config)


def get_file_type_htm_links(url, find_all_seq, count):
    # Get our url and open it with library BeautifulSoup
    req = Request(url)
    html_page = urlopen(req)
    soup = BeautifulSoup(html_page, features="lxml")

    # Initialize 2 lists, since we'll have to first get all the links, then get only the amount of links asked by user
    # This amount is given by parameter 'count'
    href_list = []
    file_link_list = []

    # Get all the links to file type
    for link in soup.findAll(find_all_seq):
        if find_all_seq is "a":
            if link.get('href').startswith("/Archives/edgar/data/"):
                href_list.append("https://www.sec.gov" + link.get('href'))
        else:
            href_list.append(link.text)

    # Get only the amount of links that the user asks for, dictated by parameter 'count'
    for data in href_list:
        if count is 0:
            break
        file_link_list.append(data)
        count -= 1

    return file_link_list


if __name__ == '__main__':
    # create_table()
    # input_company_db_list()
    # delete_all_sql_data()
    # translate_db_to_csv_file()
    # update_company_db_list()
    # test_scraping()
    # new_update_db()
    # str1 = "https://www.sec.gov/Archives/edgar/data/320193/000032019317000009/a10-qq32017712017.htm"
    # print(str1.rsplit('/', 1)[-1].rsplit('.', 1)[0])
    get_company_file_type("APPLE INC", "320193", "10-Q", 20180101, count=5)
    conn.close()
