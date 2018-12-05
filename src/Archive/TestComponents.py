from urllib.request import urlopen, Request

from bs4 import BeautifulSoup


def test_function(company_name, cik_key, file_type, prior_to, count):
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

    # archives_data_links = ['https://www.sec.gov/Archives/edgar/data/320193/000119312514277160/d740164d10q.htm', 'https://www.sec.gov/Archives/edgar/data/320193/000119312514277160/d740164dex311.htm', 'https://www.sec.gov/Archives/edgar/data/320193/000119312514277160/d740164dex312.htm', 'https://www.sec.gov/Archives/edgar/data/320193/000119312514277160/d740164dex321.htm', 'https://www.sec.gov/Archives/edgar/data/320193/000119312514277160/0001193125-14-277160.txt', 'https://www.sec.gov/Archives/edgar/data/320193/000119312514277160/aapl-20140628.xml', 'https://www.sec.gov/Archives/edgar/data/320193/000119312514277160/aapl-20140628.xsd', 'https://www.sec.gov/Archives/edgar/data/320193/000119312514277160/aapl-20140628_cal.xml', 'https://www.sec.gov/Archives/edgar/data/320193/000119312514277160/aapl-20140628_def.xml', 'https://www.sec.gov/Archives/edgar/data/320193/000119312514277160/aapl-20140628_lab.xml']
    # res = []
    for link in archives_data_links:
        res.append(get_file_type_htm_links(link, "a", int(count)))

    # Translate each htm into pdf and save it to an Annual Reports folder
    ret_dict = {}
    for html_link in res:
        req_file_type = html_link[0]
        new_pdf_file_name = "\\" + req_file_type.rsplit('/', 1)[-1].rsplit('.', 1)[0] + ".pdf"
        ret_dict[new_pdf_file_name] = req_file_type
        # self.html_to_pdf_directly(html_link,
        #                           self.current_directory,
        #                           company_name.replace(" ", ""),
        #                           file_type,
        #                           new_pdf_file_name)

    print(ret_dict)
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


if __name__ == '__main__':
    # APPLE INC
    # pisa.showLogging()
    # get_entry_text("APPLE INC", "0000320193", 20180101, 1)
    # base url for apple:
    # https://www.sec.gov/cgi-bin/browse-edgar?action=getcompany&CIK=0000320193&type=10-Q&dateb=20180101&owner=exclude&output=xml&count=10
    test_function("APPLE+INC", "0000320193", "10-Q", "20180101", "10")
