import sys
import unittest

import pandas as pd

sys.path.extend(['../..'])
from etl import cbs
from etl import PCODE_NAME
from etl import HH_NAME

class CbsTests(unittest.TestCase):

    def test_equal_vdc_list(self):
        l = []
        for v in self.pcode['VDC_NAME']:
            l.append(cbs.get_12th_approx(v))

        test_cnts = pd.Series(l).value_counts()
        act_cnts = pd.Series([v[12] for v in self.pcode['VDC_CODE']]).value_counts()

        for k, v in act_cnts.items():
            self.assertEqual(test_cnts[k], v)


    def test_add_vdc_codes(self):
        cbs.add_vdc_codes(self.hh)


    def test_non_dup_ids_hh(self):
        """make sure there aren't any duplicate UIDs in HH data"""
        with_dist = cbs.add_dist_codes(self.hh, self.pcode).loc[:, ['vdcmun', 'vcode', 'dist_code']].drop_duplicates()
        join = with_dist['dist_code'].map(str) + ' ' + with_dist['vdcmun'].map(str)

        self.assertFalse(True in join.duplicated())


    def setUp(self):
        self.hh = cbs.read_hh('../../data/' + HH_NAME)
        self.pcode = cbs.read_pcode('../../data/' + PCODE_NAME)


if __name__ == '__main__':
    unittest.main()
