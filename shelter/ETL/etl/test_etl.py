import unittest
import etl
from openpyxl import load_workbook
import os 


sample_wb = load_workbook('/Users/ewanog/code/nepal-earthquake/shelter/etl/etl_test.xlsx')
db = sample_wb.get_sheet_by_name('Database')
ref = sample_wb.get_sheet_by_name('Reference')

class TestEtl(unittest.TestCase):

    def test_find_last_value_row(self):
        self.assertEqual(etl.find_last_value(ref, 'A', 'r'), 'Z1')

    def test_find_last_value_column(self):
        self.assertEqual(etl.find_last_value(ref, 'Z', 'c'), 'Z11')

    def test_find_in_header(self):
        self.assertEqual(etl.find_in_header(ref, 'TESTINGCOL'), 'J')       

    def test_colvals_notincol(self):
        self.assertEqual(tuple(etl.colvals_notincol(db, 'A', ref, 'A')), 
            tuple(['notincluded1','notincluded2','notincluded3']))

    def test_report_a_log(self):
        etl.report_a_log('ent1', 'file1')
        etl.report_a_log('ent2', 'file1')
        etl.report_a_log('ent4', 'file2')
        etl.report_a_log('ent5', 'file2')
        etl.report_a_log('', 'text')

        assert os.path.exists('/Users/ewanog/code/nepal-earthquake/shelter/etl/etl/logs/file1.txt')
        assert os.path.exists('/Users/ewanog/code/nepal-earthquake/shelter/etl/etl/logs/file2.txt')


if __name__ == '__main__':
    unittest.main()
