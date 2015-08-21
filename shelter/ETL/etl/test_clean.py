import unittest
import etl
import clean
from openpyxl import load_workbook

sample_wb = load_workbook('/Users/ewanog/code/nepal-earthquake/shelter/etl/clean_test.xlsx')
dist = sample_wb.get_sheet_by_name('Distributions')
train = sample_wb.get_sheet_by_name('Training')
ref = sample_wb.get_sheet_by_name('Reference')

class TestClean(unittest.TestCase):
    print ''

if __name__ == '__main__':
    print clean.algo19(dist, ref)
