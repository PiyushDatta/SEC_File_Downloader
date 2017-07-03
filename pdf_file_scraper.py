
"""
Only gets annual reports from SEC website for a given CIK/Company Name
"""

# Lib to obtain data from url
from urllib import request
from bs4 import BeautifulSoup
from selenium import webdriver
from os import path, getcwd, makedirs
import csv
import requests

# Current site for CIK list (by SEC) as of June 23rd, 2017
sec_cik_url = 'https://www.sec.gov/Archives/edgar/cik-lookup-data.txt'

# Variables to call/open the files
our_cik_txt = 'CIK_List.txt'
our_cik_csv = 'CIK_List.csv'
annual_report_folder = path.join(getcwd(), 'AnnualReports')
if not path.exists(annual_report_folder):
    makedirs(annual_report_folder)


# Function to update the CIK file (in case new companies are added)
def update_cik_list(cik_url, file_format):
    """

    :param cik_url: String
    :param file_format: String
    :return: None
    """
    response = request.urlopen(cik_url)
    org_csv = response.read()
    csv_str = str(org_csv)
    csv_lines = csv_str.split('\\n')
    dest_url = r'CIK_List' + '.' + file_format
    fx = open(dest_url, "w")

    for line in csv_lines:
        fx.write(line + "\n")

    fx.close()


# Get all cik keys in a given range
def get_cik_keys(cik_txt_file, range_x, range_y):
    """

    :param cik_txt_file: String
    :param range_x: int
    :param range_y: int
    :return: int
    """
    res = []
    counter = 1
    with open(cik_txt_file) as myfile:
        for line in myfile.readlines():
            if counter >= range_x:
                cik_name = str(line.rsplit(':')[1])
                res.append(cik_name)

            if counter > range_y:
                break

            counter += 1

    return res


# Get all company names in a given range
def get_company_names(cik_txt_file, range_x, range_y):
    """

    :param cik_txt_file: String
    :param range_x: int
    :param range_y: int
    :return: int
    """
    res = []
    counter = 1
    with open(cik_txt_file) as myfile:
        for line in myfile.readlines():
            if counter >= range_x:
                comp_name = str(line.rsplit(':')[0])
                try:
                    if int(comp_name[0]) >= 0:
                        comp_name = comp_name.rsplit(" ")[1:]
                        comp_name = " ".join(comp_name)
                        comp_name = comp_name.strip('/')
                        res.append(comp_name.strip())
                except ValueError:
                    res.append(comp_name)

            if counter > range_y:
                break

            counter += 1

    return res


# Get a single company name, with a line number corresponding to cik txt file
# If you have a range, then use get_company_names function
def get_single_company_name(cik_txt_file, line_num):
    """

    :param cik_txt_file: String
    :param line_num: Integer
    :return: String
    """
    return get_company_names(cik_txt_file, line_num - 1, line_num + 1)[0]


# Get a single cik key, with a line number corresponding to cik txt file
# If you have a range, then use get_cik_keys function
def get_single_cik_key(cik_txt_file, line_num):
    """

    :param cik_txt_file: String
    :param line_num: Integer
    :return: String
    """
    return get_cik_keys(cik_txt_file, line_num - 1, line_num + 1)[0]


def get_annual_reports_pdf(save_to_folder, cik_keys):
    """

    :param save_to_folder: String
    :param cik_keys: List[String]
    # :param prior_to_date: String
    :return: None
    """
    soup_href = {}

    # Loop through all the companies
    for cik in cik_keys:

        # Access the url with all the 10ks for the company
        base_url = "http://www.sec.gov/cgi-bin/browse-edgar?action=getcompany&CIK=" + str(cik) + \
                   "&type=10-K&dateb=&owner=exclude&output=xml&count=100"
        response = requests.get(base_url)
        data = response.content

        # Get all the data from the html page, which includes the file links for the 10ks
        soup = BeautifulSoup(data, "html.parser")
        # soup_href[get]
        if not [] in soup.find_all("filinghref"):
            soup_href.append(soup.find_all("filinghref"))

    print(soup_href)


def download_file(url):
    local_filename = url.split('/')[-1]
    r = requests.get(url, stream=True)
    with open(local_filename, 'wb') as f:
        for chunk in r.iter_content(chunk_size=2000):
            # filter out keep-alive new chunks
            if chunk:
                f.write(chunk)
                # f.flush() commented by recommendation from J.F.Sebastian
    return local_filename


# Get the line number corresponding to the cik text file, given a company name (in all caps)
def get_line_number_company_name(cik_txt_file, company_name):
    """

    :param cik_txt_file: String
    :param company_name: String
    :return: Integer
    """

    line_counter = 0

    with open(cik_txt_file) as my_file:
        for file_line in my_file.readlines():
            line_counter += 1
            comp_name = str(file_line.rsplit(':')[0])
            try:
                if comp_name != "" and int(comp_name[0]) >= 0:
                    comp_name = comp_name.rsplit(" ")[1:]
                    comp_name = " ".join(comp_name)
                    comp_name = comp_name.strip('/')
                    comp_name = comp_name.strip()
                    if str(comp_name) == company_name:
                        return line_counter
            except ValueError:
                comp_name = comp_name.strip('/')
                comp_name = comp_name.strip()
                if str(comp_name) == company_name:
                    return line_counter

    return "Not Found"


# Get the line number corresponding to the cik text file, given a cik key
def get_line_number_cik_key(cik_txt_file, cik_key):
    """

    :param cik_txt_file: String
    :param cik_key: String
    :return: Integer
    """

    line_counter = 0

    cik_key = str(cik_key)
    with open(cik_txt_file) as my_file:
        for file_line in my_file.readlines():
            line_counter += 1
            try:
                cik_number = str(file_line.rsplit(':')[-2])
                if cik_number == cik_key:
                    return line_counter + 1
            except IndexError:
                continue

    return "Not Found"


# Get a dictionary of the company's name and cik key, given a line number
# that corresponds to the cik text file
def get_company_information(cik_txt_file, company_line_num):
    """
    :param cik_txt_file: String
    :param company_line_num: Integer
    :return: dict[String: String]
    """
    res = dict()

    comp_name = get_single_company_name(cik_txt_file, company_line_num)
    comp_cik = get_single_cik_key(cik_txt_file, company_line_num)

    res["CIK Key: "] = comp_cik
    res["Company Name: "] = comp_name

    return res


if __name__ == '__main__':
    range_x_1 = 35443
    range_y_1 = 35448
    print(get_line_number_company_name(our_cik_txt, "APPLE INC"))
    print(get_line_number_cik_key(our_cik_txt, "0000320193"))
    print(get_company_information(our_cik_txt, get_line_number_company_name(our_cik_txt, "APPLE INC")))

    # print(get_annual_reports_pdf(annual_report_folder, get_cik(our_cik_txt, range_x_1, range_y_1)))

    print("=======================================")
    counter = 1
    with open(our_cik_txt) as myfile:
        for line in myfile.readlines():
            if counter == 35447:
                print(get_single_company_name(our_cik_txt, 35437))
                break
            counter += 1
    print("=======================================")
    print("Number of lines in txt: " + str(662067))

# update_cik_list(sec_cik_url, 'txt')
# Have to fix formatting for csv file types
# update_cik_list(sec_cik_url, 'csv')
