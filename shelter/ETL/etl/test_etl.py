import unittest
import etl
from openpyxl import load_workbook
from openpyxl import Workbook

import os 


sample_wb_new_format = load_workbook('/Users/ewanog/code/nepal-earthquake/shelter/etl/clean_test.xlsx', data_only = True)
sample_wb = load_workbook('/Users/ewanog/code/nepal-earthquake/shelter/etl/etl_test.xlsx')
db = sample_wb.get_sheet_by_name('Database')
ref = sample_wb.get_sheet_by_name('Reference')

class TestEtl(unittest.TestCase):

    def test_wb_format_false(self):
        self.assertEqual(etl.wb_format(sample_wb), False)

    def test_wb_format_true(self):
        self.assertEqual(etl.wb_format(sample_wb_new_format), True)

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
        etl.report_a_log('**FILE 1**', 'file1')
        etl.report_a_log('ent2', 'file1')
        etl.report_a_log('ent2', 'file1')
        etl.report_a_log('**FILE 2**', 'file2')
        etl.report_a_log('ent5', 'file2')
        etl.report_a_log('ent5', 'file2')
        etl.report_a_log('**FILE 3**', 'file3')
        etl.report_a_log('ent5', 'file3')
        etl.report_a_log('ent5', 'file3')

        etl.report_a_log('', 'text')

        assert os.path.exists('/Users/ewanog/code/nepal-earthquake/shelter/etl/etl/logs/cleaned_log.txt')

    def test_consolidate(self):
        #create historical db
        db = Workbook().active
        db.append(('val', 'key'))
        db.append(('dupval1', 'dupkey1'))
        db.append(('row2val', 'key1'))
        db.append(('row3val', 'key2'))
        db.append(('dupval2', 'dupkey2'))

        #create two sheets to add
        ws1 = Workbook().active
        ws1.append(('val', 'key'))
        ws1.append(('dupval1', 'dupkey1'))
        ws1.append(('notdupedws1', 'notdupedvalws1'))
        
        ws2 = Workbook().active
        ws2.append(('val', 'key'))
        ws2.append(('dupval2', 'dupkey2'))
        ws2.append(('notdupedws2', 'notdupedvalws2'))

        cons = etl.consolidate(db, (ws1, ws2), 'B')
        cons_sheet = cons.get_sheet_by_name('Consolidated')
        self.assertEqual(set(etl.get_values(cons_sheet.columns[1])), 
            (set(['key','key1','key2','dupkey1','notdupedvalws1','dupkey2','notdupedvalws2'])))

    def test_get_values(self):
        db = Workbook().active
        db.append(('val', 'key'))
        self.assertEqual(etl.get_values(db.rows[0]),['val','key'])


if __name__ == '__main__':
    unittest.main()
