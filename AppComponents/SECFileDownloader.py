"""
Gets company reports/files from SEC website for a given CIK/Company Name.
Currently only gets 10ks (Annual reports).
"""

# Lib to obtain data from url

import argparse
import os

import pdfkit
from bs4 import BeautifulSoup
from os import path, getcwd, makedirs
import errno
import requests
import sys
from urllib.request import urlopen, Request

# Get methods from SQL db file
from AppComponents import SEC_sql_database as my_sql


class FileDownloader:

    def __init__(self, current_dir, selected_company):

        # Current site for CIK list (by SEC) as of June 23rd, 2017
        self.sec_cik_url = 'https://www.sec.gov/Archives/edgar/cik-lookup-data.txt'

        # Current directory to save files into
        self.current_directory = current_dir

        # Config file
        parent_path = os.path.abspath(os.path.join(os.getcwd(), os.pardir))
        self.wkhtmltopdf_config_file = path.join(parent_path, "wkhtmltopdf\\bin\\wkhtmltopdf.exe")

        # Variables to call/open the files
        self.download_sec_file_counter = 1
        # our_cik_txt = 'CIK_List.txt'
        # our_cik_csv = 'CIK_List.csv'
        self.company = selected_company
        # self.company = selected_company.get_chosen_company_cik_key()

        # Annual reports folder
        self.annual_report_folder = path.join(current_dir, 'AnnualReports')
        if not path.exists(self.annual_report_folder):
            try:
                makedirs(self.annual_report_folder)
            except OSError as exception:
                if exception.errno != errno.EEXIST:
                    raise

        # Current platform
        self.current_platform = self.get_platform()

    def get_platform(self):
        platforms = {
            'linux1': 'Linux',
            'linux2': 'Linux',
            'darwin': 'OS X',
            'win32': 'Windows'
        }
        if sys.platform not in platforms:
            return 'Other'

        return platforms[sys.platform]

    def get_range_cik_keys_from_db(self, range_x, range_y):
        """
        Return only the CIK keys of companies in range x to range y (inclusive) in a list

        :param range_x: Integer
        :param range_y: Integer
        :return: List[Integer]
        """
        res = list()

        for comp in my_sql.get_range_of_cik_keys(range_x, range_y):
            res.append(comp[-1])

        return res

    def get_single_company_from_cik(self, cik_key):
        """

        :param cik_key: Integer
        :return: String
        """
        return my_sql.get_company_by_cik_key(cik_key)

    def get_single_company_from_name(self, company_name):
        """

        :param company_name: String
        :return: String
        """
        return my_sql.get_company_by_name(company_name)

    def get_cik_key_from_ticker(self, ticker_symbol):
        """

        :param ticker_symbol: String
        :return: String
        """
        return my_sql.get_company_by_name(ticker_symbol)

    def get_annual_reports_pdf(self, save_to_folder, cik_keys):
        """

        :param save_to_folder: String
        :param cik_keys: List[Integer]
        # :param prior_to_date: String
        :return: None
        """
        soup_href = {}
        global download_sec_file_counter

        # Loop through all company cik keys
        for cik in cik_keys:
            # Access the url for the company name
            comp_url = "https://www.sec.gov/cgi-bin/browse-edgar?action=getcompany&CIK=" + str(cik)
            comp_response = requests.get(comp_url)
            comp_data = comp_response.content
            comp_soup = BeautifulSoup(comp_data, "html.parser")
            # Get the current company name, related to the given CIK key
            comp_name = str(comp_soup.find('span', {"class": "companyName"}).next)

            # Access the url with all the 10ks for the company
            base_url = "http://www.sec.gov/cgi-bin/browse-edgar?action=getcompany&CIK=" + str(cik) + \
                       "&type=10-K&dateb=&owner=exclude&output=xml&count=100"
            response = requests.get(base_url)
            data = response.content
            # Get all the data from the html page, which includes the file links for the 10ks
            soup = BeautifulSoup(data, "html.parser")
            # Add all the 10k links to a dict, with the company name being the key
            soup_href[comp_name] = (soup.find_all("filinghref"))

        print("===== Done scraping for the companies! =====")

        # Only retain companies with a 10k (not empty list)
        file_dict = dict()
        for cmp in soup_href:
            if soup_href[cmp]:
                file_dict[cmp] = soup_href[cmp]

        # Separate each url in dict, and then add it to a list, include company names
        file_list = list()
        for current_company in file_dict:
            file_list.append([current_company])
            for link in file_dict[current_company]:
                str_link = str(link).split("<filinghref>", 1)[-1].split("</filinghref>")[0]
                file_list.append(str_link)

        print("===== Downloading now... =====")
        # Download the files
        current_folder = self.annual_report_folder
        for link in file_list:
            # Check the company names, so a company folder can be made for the next set of files
            # Else, download the files in current folder
            if isinstance(link, list):
                saving_folder = path.join(save_to_folder, "".join(link[0].split()))
                if not path.exists(saving_folder):
                    makedirs(saving_folder)
                current_folder = saving_folder
                download_sec_file_counter = 1
                print("Made folder: " + current_folder)
            # It is a file, download it to current folder
            else:
                self.download_sec_file(current_folder, link)
                print("Downloaded into: " + current_folder)

    def download_sec_file(self, output_folder, url):
        """
        Output folder = SEC_file_downloader\AnnualReports
        :param output_folder:
        :param url:
        :return:
        """
        sec_url = "https://www.sec.gov"
        response = requests.get(url)
        base_data = response.content
        base_soup = BeautifulSoup(base_data, "html.parser")
        global download_sec_file_counter, file_name

        for tag in base_soup.find_all('td', {'scope': 'row'}):
            children = tag.findChildren()
            if len(children) > 0:
                file_name = children[0]['href']
                break

        whole_link = sec_url + file_name
        output_filename = file_name.split('/')[-1]

        # if output_filename.split('.')[-1] == "htm" or out.split('.')[-1] == "html":
        # config = pdfkit.configuration(wkhtmltopdf="%r" % wkhtmltopdf_config_file)
        config = pdfkit.configuration(wkhtmltopdf=self.wkhtmltopdf_config_file)
        # config = pdfkit.configuration(wkhtmltopdf=
        #                               r"C:\Users\Piyush\Documents\Programming\SEC_file_downloader\wkhtmltopdf_config\Windows\wkhtmltox-0.12.4_msvc2015-win32.exe")
        output_filename = file_name.split('/')[-1]

        if len(output_filename) >= 4:
            try:
                if int(output_filename[-4:]):
                    output_filename = output_folder.split("\\")[-1] + "_10k_" + output_filename[-4:]
            except ValueError:
                output_filename = output_folder.split("\\")[-1] + "_10k_UNKNOWN_DATE" + "_" + \
                                  str(download_sec_file_counter)
                download_sec_file_counter += 1
        elif len(output_filename) == 0:
            output_filename = output_folder.split("\\")[-1] + "_DIRECTORY_LIST_IGNORE"
        else:
            output_filename = output_folder.split("\\")[-1] + "_10k_UNKNOWN_DATE" + "_" + \
                              str(download_sec_file_counter)
            download_sec_file_counter += 1

        print("==============")
        print(output_filename)
        print("==============")
        output = output_folder + '\\' + output_filename + ".pdf"
        ann_folder = self.annual_report_folder + '\\' + output_filename.split('.')[0] + ".pdf"
        if path.exists(output_folder):
            pdfkit.from_url(whole_link, output, configuration=config)
        else:
            pdfkit.from_url(whole_link, ann_folder, configuration=config)
            # else:
            #     pass
            # Might download to non-pdf format in the future
            # download_url_non_pdf_format(save_folder, new_link, local_filename)

    def download_url_non_pdf_format(self, save_folder, whole_link, file_name):
        """
        # DO NOT USE, MADE JUST IN CASE
        :param save_folder:
        :param whole_link:
        :param file_name:
        :return:
        """
        response = requests.get(whole_link, stream=True)

        # Throw an error for bad status codes
        response.raise_for_status()

        with open(file_name, 'wb') as handle:
            for block in response.iter_content(1024):
                handle.write(block)

    def get_company_file_type(self, company_name, cik_key, file_type, prior_to, count=10):
        # Generate the url to crawl
        base_url = "http://www.sec.gov/cgi-bin/browse-edgar?action=getcompany&CIK=" + str(
            cik_key) + "&type=" + str(file_type) + "&dateb=" + str(prior_to) + "&owner=exclude&output=xml&count=" + str(
            count)

        print("Base url we are trying to scrape for file types: " + base_url)

        # Where the links to the htm files that need to be translated into pdf will go
        res = []

        # Get links to type of files for company
        archives_data_links = self.get_file_type_htm_links(base_url, "filinghref", int(count))

        # Get the actual htm of the type of file for the company
        for link in archives_data_links:
            res = self.get_file_type_htm_links(link, "a", int(count))

        # Translate each htm into pdf and save it to an Annual Reports folder
        for html_link in res:
            new_pdf_file_name = "\\" + html_link.rsplit('/', 1)[-1].rsplit('.', 1)[0] + ".pdf"
            self.html_to_pdf_directly(html_link,
                                      self.current_directory,
                                      company_name.replace(" ", ""),
                                      file_type,
                                      new_pdf_file_name)

        print()
        print("Printed all " + file_type + " for: " + company_name + "!")

    def html_to_pdf_directly(self, request, parent_path, company_name, file_type, pdf_file_name):
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

    def get_file_type_htm_links(self, url, find_all_seq, count):
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

    def set_current_directory(self, new_dir):
        self.current_directory = new_dir

    def set_current_company(self, new_company):
        self.company = new_company
