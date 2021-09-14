from PySheetAdaptor.Tests.test import PysheetAdaptorTestCases
import unittest

if __name__ == "__main__":

    suite = unittest.TestSuite()
    suite.addTest(PysheetAdaptorTestCases("test_open_spreadsheet"))
    suite.addTest(PysheetAdaptorTestCases("test_create_worksheet"))
    suite.addTest(PysheetAdaptorTestCases("test_open_worksheet"))
    suite.addTest(PysheetAdaptorTestCases("test_set_columns"))
    suite.addTest(PysheetAdaptorTestCases("test_insert_method"))
    suite.addTest(PysheetAdaptorTestCases("test_insert_at"))
    suite.addTest(PysheetAdaptorTestCases("test_append_func"))
    suite.addTest(PysheetAdaptorTestCases("test_delete_at_func"))
    suite.addTest(PysheetAdaptorTestCases("test_update_func"))
    suite.addTest(PysheetAdaptorTestCases("test_get_record_func"))

    runner = unittest.TextTestRunner()
    runner.run(suite)