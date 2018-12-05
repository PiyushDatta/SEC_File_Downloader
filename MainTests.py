import unittest
from src.AppComponents.AppComponentsTest.CompanyTest import CurrentCompanyTest


def main():
    # Put test class here
    test_classes_to_run = [CurrentCompanyTest]

    loader = unittest.TestLoader()

    suites_list = []
    for test_class in test_classes_to_run:
        suite = loader.loadTestsFromTestCase(test_class)
        suites_list.append(suite)

    big_suite = unittest.TestSuite(suites_list)

    runner = unittest.TextTestRunner()
    results = runner.run(big_suite)


if __name__ == '__main__':
    main()
