import logging
import unittest
from PySheetAdaptor.PySheetAdaptor import PySheetAdaptor


class PysheetAdaptorTestCases(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.report= logging.getLogger('Report')
        cls.report.setLevel(logging.CRITICAL)
        cls.consoleHandler = logging.StreamHandler()
        cls.consoleHandler.setLevel(logging.CRITICAL)
        cls.consoleFormatter = logging.Formatter(f"@Testing : %(levelname)s- %(message)s" ,datefmt='%Y-%m-%d => %H:%M ')
        cls.consoleHandler.setFormatter(cls.consoleFormatter)
        cls.report.addHandler(cls.consoleHandler)
        global test_adaptor
        test_adaptor = PySheetAdaptor(AUTO_LOGIN = {"username":"srihari", "password":"pass"})
        global records
        records = [
                ["Cognizent", "US", 200000, 125, 1245354, 1500000000, "12\09\21"],
                ["Accenture", "UK", 300000, 145, 1246554, 2000000000, "14\09\21"],
                ["TCS", "IND", 1000000, 125, 13245354, 10000000000, "16\05\21"],
                ["Capgemini", "CND", 100000, 105, 124534, 10000000, "12\09\21"],
                ["Amazon", "US", 500000, 245, 8756756, 2500000000, "12\09\20"],
                ["facebook", "US", 769878, 235, 1245354, 2500000000, "12\09\21"],
                ["Google", "IND", 500000, 300, 9879887, 4500000000, "22\06\21"],
                ["Netflix", "UK", 200000, 125, 6546444, 500000000, "20\11\21"],
                ["IBM", "US", 300000, 225, 5454544, 1500000000, "18\09\21"],
                ["Wipro", "IND", 100000, 115, 5456445, 500000000, "05\09\21"],
            ]
        global columns
        columns = ["CompanyName", "Location", "noOfEmployees", "Growth", "Revenue", "Shares", "JoinDate"]

    @classmethod
    def tearDownClass(cls) -> None:
        pass

    def doCleanups(self) -> None:
        pass

    @classmethod
    def doClassCleanups(cls) -> None:
        pass

    def setUp(self) -> None:
        pass

    def tearDown(self) -> None:
        pass

    def test_create(self):
        # *** Running the TestCases.....
        self.assertEqual(test_adaptor.open_spreadsheet(url="wrong_url"),False)
        self.assertEqual(test_adaptor.open_spreadsheet(title="NoTitle"),False)
        self.assertEqual(test_adaptor.open_spreadsheet(url=test_adaptor.test_spreadsheet_url),True)

    def test_open_spreadsheet(self):
        self.assertEqual(test_adaptor.open_spreadsheet(url="wrong_url"),False)
        self.assertEqual(test_adaptor.open_spreadsheet(title="NoTitle"),False)
        self.assertEqual(test_adaptor.open_spreadsheet(url=test_adaptor.test_spreadsheet_url),True)

    def test_create_worksheet(self):
        self.assertEqual(test_adaptor.create_worksheet(title="testsheet"),False)
        self.assertEqual(test_adaptor.create_worksheet(title="NewSheet"),True)
        self.assertEqual(test_adaptor.create_worksheet(),True)

    def test_open_worksheet(self):
        self.assertEqual(test_adaptor.open_worksheet(title="NoSheetFound"),False)
        self.assertEqual(test_adaptor.open_worksheet(title="NoTitle"),False)
        self.assertEqual(test_adaptor.open_worksheet(title="testsheet"),True)

    def test_set_attributes(self):
        self.assertEqual(test_adaptor.set_columns(columns=columns),True)

    def test_insert_method(self):
        for record in records:
            self.assertEqual(test_adaptor.insert_record(record=record), True)
        self.assertEqual(test_adaptor.insert_record(record=[]),False)
        self.assertEqual(test_adaptor.insert_record(record=["uethuiy", "efhoieghor"]),False)

    def test_search_record(self):
        for record in records:
            self.assertEqual(test_adaptor.search_record(CompanyName=record[0]), record)
        self.assertEqual(test_adaptor.search_record(companyName="Wipro"),None)
        self.assertEqual(test_adaptor.search_record(CompanyName="Wiproind"),None)
        self.assertEqual(test_adaptor.search_record(),None)

