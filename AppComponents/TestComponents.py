import requests
from lxml import html


def get_entry_text(chosen_company_str):
    print("Chosen company: " + chosen_company_str)
    # https://www.sec.gov/cgi-bin/browse-edgar?CIK=qwe&owner=exclude&action=getcompany

    cik_url = "https://www.sec.gov/cgi-bin/browse-edgar?CIK=" + str(
        chosen_company_str) + "&owner=exclude&action=getcompany"

    # SEC doesn't use spaces, they use the + sign in place of any spaces
    chosen_company_str.replace(" ", "+")

    company_name_url = "https://www.sec.gov/cgi-bin/browse-edgar?company=" + str(
        chosen_company_str) + "&owner=exclude&action=getcompany"

    company_name = []

    page = requests.get(cik_url)
    tree = html.fromstring(page.content)
    company_name = tree.xpath('//span[@class="companyName"]/text()')

    if not company_name:
        page = requests.get(company_name_url)
        tree = html.fromstring(page.content)
        company_name = tree.xpath('//span[@class="companyName"]/text()')
        if not company_name:
            return "Could not retrieve"

    return company_name[0]

    # if chosen_company_str in company_listing and chosen_company_str:
    #     self.current_company = chosen_company_str


if __name__ == '__main__':
    print(get_entry_text('APPLE INC'))
