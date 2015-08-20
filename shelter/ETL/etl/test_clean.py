import unittest
import etl
import clean
from openpyxl import load_workbook

sample_wb = load_workbook('/Users/ewanog/code/nepal-earthquake/shelter/etl/clean_test.xlsx')
dist = sample_wb.get_sheet_by_name('Distributions')
train = sample_wb.get_sheet_by_name('Training')
ref = sample_wb.get_sheet_by_name('Reference')

class TestClean(unittest.TestCase):

    def test_algo1(self):
        self.assertEqual(clean.algo1(dist, ref), 'The following agencies are not in the reference:\nMedair-MissionEastHH')

    def test_algo2(self):
        self.assertEqual(clean.algo2(dist, ref), 'The following rows were marked as internal:\n3')


if __name__ == '__main__':
    unittest.main()