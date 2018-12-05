"""
Gets company reports/files from SEC website for a given CIK/Company Name.
Currently only gets 10ks (Annual reports).
"""

# Lib to obtain data from url

import os
import sys
from os import path
from urllib.request import urlopen, Request

import pdfkit
from bs4 import BeautifulSoup


class FileDownloader:

    def __init__(self, current_dir, selected_company):

        # Current site for CIK list (by SEC) as of June 23rd, 2017
        # Note used, but good to have for the future
        self.sec_cik_url = 'https://www.sec.gov/Archives/edgar/cik-lookup-data.txt'

        # Current directory to save files into
        self.current_directory = current_dir

        # Our parent path is the src folder
        self._parent_path = os.getcwd() + '\\src'
        self.wkhtmltopdf_config_file = path.join(self._parent_path, "wkhtmltopdf\\bin\\wkhtmltopdf.exe")

        # Variables to call/open the files
        self.company = selected_company

        # Current platform
        self.current_platform = get_platform()

    def set_current_directory(self, new_dir):
        self.current_directory = new_dir

    def set_current_company(self, new_company):
        self.company = new_company

    def html_to_pdf_directly(self, request, company_name, file_type, pdf_file_name):
        # Config path to wkhtmltopdf, this exe file is needed for pdfkit
        config = pdfkit.configuration(wkhtmltopdf=self.wkhtmltopdf_config_file)

        # Where we will save our files
        annual_reports_path = self.current_directory + "\\AnnualReports"
        company_path = annual_reports_path + "\\" + company_name
        type_path = company_path + "\\" + file_type

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

        # If type folder under company folder doesn't exist , make it
        if not os.path.exists(type_path):
            os.mkdir(type_path)
            print("Directory: ", type_path, " == Created ")
        else:
            print("Directory: ", type_path, " == Already exists")

        print("Path of file we are converting: " + type_path + pdf_file_name)

        # Get the url link to the file type and convert it into pdf
        pdfkit.from_url(request, type_path + pdf_file_name, configuration=config)

    def get_company_file_type(self, file_type, prior_to, count=10):

        cik_key = self.company.get_chosen_company_cik_key()

        # Generate the url to crawl
        base_url = "http://www.sec.gov/cgi-bin/browse-edgar?action=getcompany&CIK=" + str(
            cik_key) + "&type=" + str(file_type) + "&dateb=" + str(prior_to) + "&owner=exclude&output=xml&count=" + str(
            count)

        print("Base url we are trying to scrape for file types: " + base_url)

        # Where the links to the htm files that need to be translated into pdf will go
        res = []

        # Get links to type of files for company
        archives_data_links = get_file_type_htm_links(base_url, "filinghref", int(count))

        # Get the actual htm of the type of file for the company
        for link in archives_data_links:
            res.append(get_file_type_htm_links(link, "a", int(count)))

        # Translate each htm into pdf and save it to an Annual Reports folder
        ret_dict = {}
        for html_link in res:
            req_file_type = html_link[0]
            new_pdf_file_name = "\\" + req_file_type.rsplit('/', 1)[-1].rsplit('.', 1)[0] + ".pdf"
            ret_dict[new_pdf_file_name] = req_file_type

        print("Put file links into dict!")
        return ret_dict


def get_file_type_htm_links(url, find_all_seq, count):
    # Get our url and open it with library BeautifulSoup
    req = Request(url)
    html_page = urlopen(req)
    soup = BeautifulSoup(html_page, features="lxml")

    # Initialize 2 lists, since we'll have to first get all the links, then get only the amount of links asked by
    #  user. This amount is given by parameter 'count'
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


def get_platform():
    platforms = {
        'linux1': 'Linux',
        'linux2': 'Linux',
        'darwin': 'OS X',
        'win32': 'Windows'
    }
    if sys.platform not in platforms:
        return 'Other'

    return platforms[sys.platform]
