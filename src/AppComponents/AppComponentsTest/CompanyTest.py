import unittest
from AppComponents.Company import CurrentCompany


class CurrentCompanyTest(unittest.TestCase):
    def setUp(self):
        self.company = CurrentCompany("AAPL", "0000320193")
        self.getter_company = CurrentCompany("TEST", "000032019312")
        self.getter_company_two = CurrentCompany(" ", " ")
        self.getter_company_three = CurrentCompany("", "")

    def test_get_chosen_company_name(self):
        self.assertEqual(self.getter_company.get_chosen_company_name(), "TEST")
        self.assertEqual(self.getter_company_two.get_chosen_company_name(), " ")
        self.assertEqual(self.getter_company_three.get_chosen_company_name(), None)

    def test_set_company_name(self):
        self.company.set_company_name("hello")
        self.assertEqual(self.company.get_chosen_company_name(), "hello")
        self.company.set_company_name(" ")
        self.assertEqual(self.company.get_chosen_company_name(), " ")
        self.company.set_company_name("")
        self.assertEqual(self.company.get_chosen_company_name(), None)

    def test_get_chosen_company_cik_key(self):
        self.assertEqual(self.getter_company.get_chosen_company_cik_key(), "000032019312")
        self.assertEqual(self.getter_company_two.get_chosen_company_cik_key(), " ")
        self.assertEqual(self.getter_company_three.get_chosen_company_cik_key(), None)

    def test_set_company_cik_key(self):
        self.company.set_company_cik_key("hello")
        self.assertEqual(self.company.get_chosen_company_cik_key(), "hello")
        self.company.set_company_cik_key("0000134512354")
        self.assertEqual(self.company.get_chosen_company_cik_key(), "0000134512354")
        self.company.set_company_cik_key(" ")
        self.assertEqual(self.company.get_chosen_company_cik_key(), " ")
        self.company.set_company_cik_key("")
        self.assertEqual(self.company.get_chosen_company_cik_key(), None)


if __name__ == '__main__':
    unittest.main()
