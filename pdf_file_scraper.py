"""
Only gets annual reports from SEC website for a given CIK/Company Name
"""

# Lib to obtain data from url
from company_information import Company
import pdfkit
from urllib import request
from bs4 import BeautifulSoup
from selenium import webdriver
from os import path, getcwd, makedirs
import csv
import requests
# Get methods from SQL db file
import SEC_sql_database as my_sql

# Current site for CIK list (by SEC) as of June 23rd, 2017
sec_cik_url = 'https://www.sec.gov/Archives/edgar/cik-lookup-data.txt'

# Variables to call/open the files
download_sec_file_counter = 1
our_cik_txt = 'CIK_List.txt'
our_cik_csv = 'CIK_List.csv'
annual_report_folder = path.join(getcwd(), 'AnnualReports')
if not path.exists(annual_report_folder):
    makedirs(annual_report_folder)


def get_range_cik_keys_from_db(range_x, range_y):
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


def get_single_company_from_cik(cik_key):
    """

    :param cik_key: Integer
    :return: String
    """
    return my_sql.get_company_by_cik_key(cik_key)


def get_annual_reports_pdf(save_to_folder, cik_keys):
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
    current_folder = annual_report_folder
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
            download_sec_file(current_folder, link)
            print("Downloaded into: " + current_folder)


def download_sec_file(output_folder, url):
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
    global download_sec_file_counter

    for tag in base_soup.find_all('td', {'scope': 'row'}):
        children = tag.findChildren()
        if len(children) > 0:
            file_name = children[0]['href']
            break

    whole_link = sec_url + file_name
    output_filename = file_name.split('/')[-1]

    # if output_filename.split('.')[-1] == "htm" or out.split('.')[-1] == "html":
    config = pdfkit.configuration(wkhtmltopdf=r"C:\\Program Files\\wkhtmltopdf\\bin\\wkhtmltopdf.exe")
    output_filename = output_filename.split('.')[0]

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
    ann_folder = annual_report_folder + '\\' + output_filename.split('.')[0] + ".pdf"
    if path.exists(output_folder):
        pdfkit.from_url(whole_link, output, configuration=config)
    else:
        pdfkit.from_url(whole_link, ann_folder, configuration=config)
        # else:
        #     pass
        # Might download to non-pdf format in the future
        # download_url_non_pdf_format(save_folder, new_link, local_filename)


def download_url_non_pdf_format(save_folder, whole_link, file_name):
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


if __name__ == '__main__':
    range_x1 = 10000
    range_y1 = 10010
    cik_keys1 = get_range_cik_keys_from_db(range_x1, range_y1)

    get_annual_reports_pdf(annual_report_folder, cik_keys1)


    # new_link = "https://www.sec.gov/Archives/edgar/data/1085621/000089322001000425/w47166e10-k.txt"
    # save_folder = "G:\\Piyush\\aaSelf_Programming\\aaPython\\SEC_file_downloader\\AnnualReports\\ActuaCorp"
    # local_filename = new_link.split('/')[-1]
    # output = save_folder + '\\' + local_filename.split('.')[0] + ".pdf"
    # ann_folder = annual_report_folder + '\\' + local_filename.split('.')[0] + ".pdf"
    # config = pdfkit.configuration(wkhtmltopdf=r"C:\\Program Files\\wkhtmltopdf\\bin\\wkhtmltopdf.exe")
    # pdfkit.from_url(new_link, output, configuration=config)
