import os
import re
from os import path

import pdfkit
import requests
from bs4 import BeautifulSoup
from lxml import html
from urllib.request import urlopen, Request

from xhtml2pdf import pisa
from io import StringIO
import django
from django.template.loader import get_template
from django.template import Context
from django.http import HttpResponse
from django_xhtml2pdf.utils import generate_pdf

from subprocess import Popen, PIPE, STDOUT
import PyQt4

import sys


def test_function(company_name, cik_name):
    cik_url = "https://www.sec.gov/cgi-bin/browse-edgar?CIK=" + str(
            company_name) + "&owner=exclude&action=getcompany"
    company = None
    cik_key = None

    # company_url = "https://www.sec.gov/cgi-bin/browse-edgar?company=" + str(
    #     company_name) + "&owner=exclude&action=getcompany"
    print(cik_url)
    req = Request(cik_url)
    # req = Request(company_url)
    html_page = urlopen(req).read()
    soup = BeautifulSoup(html_page, features="lxml")
    links = soup.find_all("span", {"class": "companyName"})

    if len(links) is 0:
        return

    company = str(links[0].text.split("CIK#:")[0]).strip()
    cik_key = str(links[0].text.split("CIK#:")[1]).strip().split(" ", 1)[0]
    print(company)
    print(cik_key)


# https://www.sec.gov/cgi-bin/viewer?action=
# view&cik=320193&accession_number=0001628280-17-004790&xbrl_type=v

# documentsbutton

# https://www.sec.gov/Archives/edgar/data/320193/000032019318000100/0000320193-18-000100-index.htm
# 2016-06-25
# https://www.sec.gov/Archives/edgar/data/320193/000162828016017809/0001628280-16-017809-index.htm
def get_entry_text(company_code, cik_key, prior_to, count):
    # generate the url to crawl
    base_url = "http://www.sec.gov/cgi-bin/browse-edgar?action=getcompany&CIK=" + str(
        cik_key) + "&type=10-Q&dateb=" + str(prior_to) + "&owner=exclude&output=xml&count=" + str(count)

    check_url = "https://www.sec.gov/cgi-bin/browse-edgar?action=getcompany&CIK=0000320193&type=10-Q&dateb=20180101" \
                "&owner=exclude&count=10 "

    c = test_fun(check_url, "/Archives/edgar/data/")
    res = []

    for link in c:
        res.append(test_fun("https://www.sec.gov" + link, "/Archives/edgar/data/", count=1))

    checker = "https://www.sec.gov" + res[0]
    # current_dir = os.path.abspath(os.path.join(os.getcwd(), os.pardir))
    # wkhtmltopdf_config_file = path.join(current_dir, "wkhtmltopdf\\bin\\wkhtmltopdf.exe")
    # pdfkit.configuration(wkhtmltopdf=wkhtmltopdf_config_file)
    # pdf = weasyprint.HTML(checker).write_pdf()
    # pdfkit.from_url(checker, 'check_report.pdf')
    # with (os.path.join('/path/to/Documents', 'testing.pdf'), 'w') as file:
    #     file.write(pdf)
    # for data in c:
    #     if data.startswith("/Archives/edgar/data/"):
    #         new_url = "https://www.sec.gov" + data
    #         new_req = Request(check_url)
    #         new_html_page = urlopen(new_req)

    # print(data)
    # if data.startswith('<a href="/Archives/edgar/data/"'):
    #     print(data)

    # print("Successfully downloaded all the files")

    html_to_pdf_directly(checker)


def html_to_pdf_directly(request):
    path = os.path.abspath(os.path.join(os.getcwd(), os.pardir)) + "\\wkhtmltopdf\\bin\\wkhtmltopdf.exe"
    config = pdfkit.configuration(wkhtmltopdf=path)
    pdfkit.from_url(request, 'out.pdf', configuration=config)


def test_fun(url, href_link, count=0):
    req = Request(url)
    html_page = urlopen(req)
    soup = BeautifulSoup(html_page)
    c = []
    ret = []

    for link in soup.findAll("a"):
        c.append(link.get('href'))

    for data in c:
        if data.startswith("/Archives/edgar/data/"):
            ret.append(data)

    if count is 1:
        return ret[0]
    else:
        return ret


def create_document_list(data):
    # parse fetched data using beatifulsoup
    soup = BeautifulSoup(data)
    # store the link in the list
    link_list = list()

    # If the link is .htm convert it to .html
    for link in soup.find_all('filinghref'):
        url = link.string
        if link.string.split(".")[len(link.string.split(".")) - 1] == "htm":
            url += "l"
        link_list.append(url)
    link_list_final = link_list

    print("Number of files to download {0}".format(len(link_list_final)))
    print("Starting download....")

    # List of url to the text documents
    doc_list = list()
    # List of document names
    doc_name_list = list()

    # Get all the doc
    for k in range(len(link_list_final)):
        required_url = link_list_final[k].replace('-index.html', '')
        txtdoc = required_url + ".txt"
        docname = txtdoc.split("/")[-1]
        doc_list.append(txtdoc)
        doc_name_list.append(docname)
    return doc_list, doc_name_list


def save_in_directory(company_code, cik, priorto, doc_list, doc_name_list, filing_type):
    # Save every text document into its respective folder
    global filehandle
    for j in range(len(doc_list)):
        base_url = doc_list[j]
        r = requests.get(base_url)
        data = r.text
        path = os.path.join(os.getcwd(), 'AnnualReports')
        try:
            filehandle = open(path, 'ab')
        except IOError:
            print("Unable to write to file " + path)
            # sys.exit('Unable to write to file ' + path)

        filehandle.write(data.encode('ascii', 'ignore'))


if __name__ == '__main__':
    # APPLE INC
    # pisa.showLogging()
    # get_entry_text("APPLE INC", "0000320193", 20180101, 1)
    test_function("APPLE+INC", "0000320193")
