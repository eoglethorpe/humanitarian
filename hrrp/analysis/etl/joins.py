"""methods for creating merged nra dataset"""
#TODO: make 0s



from pandas import DataFrame, read_csv, read_sql

import pandas as pd
import sys
import numpy as np
import scipy.stats
from fuzzywuzzy import fuzz
from fuzzywuzzy import process

sys.path.extend(['.', '..'])
from etl import cbs

import logging
logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)
logger = logging.getLogger(__name__)



class Dataset(object):
    """data library, includes:
        CBS baseline data [coded, joined with OCHA pcode info]
        HH recon progress as of Oct 23, 2017
        """
    def __init__(self):
        self.pcode = cbs.read_pcode('../data/' + cbs.etl.PCODE_NAME)
        self.hh = pd.read_csv('../data/coded_hh.csv')
        self.lookup = pd.read_csv('../data/nra_5w_lookup.csv')
        self.nra = pd.read_csv('../data/public_vdc_assessment.csv')
        self.debug = True

        self.priority_nms = ['Bhaktapur',
                            'Kathmandu',
                            'Lalitpur',
                            'Okhaldhunga',
                            'Sindhuli',
                            'Ramechhap',
                            'Dolakha',
                            'Sindhupalchok',
                            'Kabhrepalanchok',
                            'Nuwakot',
                            'Rasuwa',
                            'Dhading',
                            'Makawanpur',
                            'Gorkha']

        self.prep_data()

    def prep_data(self):
        self.pcode = self.pcode.rename(columns={'DONTUSE_OCHA_VCODE': 'vcode', 'DIST_CODE': 'dist_code'})

        self.lookup = self.lookup[[c for c in self.lookup.columns if not c.lower().startswith('unnamed')]]
        self.lookup = self.lookup.rename(
            columns={'HRRP Code': 'hrrp_code', 'HLCIT Code': 'hlcit_code', 'VDC': 'vdc', 'Distrct': 'district'})

        self.nra['concat'] = self.nra['district'] + self.nra['vdc_municipality']

        self.pcode.columns = [v + '_pc' for v in self.pcode.columns]
        self.hh.columns = [v + '_hh' for v in self.hh.columns]
        self.lookup.columns = [v + '_look' for v in self.lookup.columns]
        self.nra.columns = [v + '_nra' for v in self.nra.columns]

    def get_nra(self):
        """join of:
                CBS baseline data -- PK: concat(distrct, vdc_code)
                OCHA pcode table -- PK1: concat(distrct, vdc_code), PK2: hlcit_code
                NRA lookup table -- PK1: hlcit_code, PK2: concat(dist_name, vdc_name) [yes, this]
                NRA VDC level reconstruction data: PK: concat(dist_name, vdc_name) [yes, still this]

            output:
                NRA VDC level reconstruction merged with CBS baseline data
                """

        if self.debug:
            self.check_hh_pc_cnts()

        self.master = self.nra
        hh_pc_mrg = self.join_hh_pcode()
        hh_pc_look_mrg = pd.merge(self.lookup, hh_pc_mrg, left_on='hlcit_code_look', right_on='hclit_code_pc', how='left')
        nra = pd.merge(self.nra, hh_pc_look_mrg, left_on = 'concat_nra', right_on = 'concat_look',
                       how = 'left', suffixes=['_nra', '_look'])
        return nra

        # nra['dist_hh_look'].isnull().sum()

    def group_hh(self):
        """group household data, get wanted columns, create dist + vdc col"""
        tmp_hh = self.hh

        if 'Unnamed: 0' in tmp_hh.columns:
            tmp_hh = tmp_hh.drop('Unnamed: 0', axis = 1)

        gc = ['dist_code_hh', 'vdcmun_hh', 'vcode_hh', 'dist_hh', 'income_hh']
        tmp_hh = pd.DataFrame(tmp_hh[gc].groupby(gc, as_index = False).size().unstack(fill_value = 0))

        tmp_hh = pd.DataFrame(tmp_hh.to_records())
        tmp_hh.columns = [v.strip("(0, ").strip("')") for v in tmp_hh.columns]
        tmp_hh = tmp_hh.rename(columns = {'10 to 20 thousands' : 'inc_10to20_hh', '20 to 30 thousands' : 'inc_20to30_hh',
                                        '30 to 50 thousands' : 'inc_30to50_hh', 'Less than 10 thousands' : 'inc_0to10_hh',
                                        'more than 50 thousands' : 'inc_greater50_hh'})

        # # str concat workout for join, probably could be fixed with multi column join but weird error
        tmp_hh['mrg_hh'] = tmp_hh['dist_code_hh'] + tmp_hh['vdcmun_hh'].apply(str)

        return tmp_hh

    def join_hh_pcode(self):
        p_sm = self.pcode[['vcode_pc', 'dist_code_pc', 'VDC_NAME_pc', 'VDC_CODE_pc', 'DIST_NAME_pc']]
        #grab the vdc number from the pcode
        p_sm['mrg_pc'] = p_sm['dist_code_pc'] + p_sm['vcode_pc'].apply(lambda x: str(int(x.split('-')[-1])))

        hh_sm = self.group_hh()

        hh_pc_mrg = pd.merge(hh_sm, p_sm, left_on='mrg_hh', right_on='mrg_pc', how='left', suffixes=['_hh', '_pc'])
        hh_pc_mrg['priority_hh'] = hh_pc_mrg.apply(lambda x: True if x['DIST_NAME_pc'] in self.priority_nms else False, axis=1)

        if self.debug:
            self.log_msg('Counts of nulls in merge of CBS, OCHA pcodes', hh_pc_mrg.isnull().sum())

        hh_pc_mrg = hh_pc_mrg.drop(['dist_code_pc'], axis=1)
        hh_pc_mrg = hh_pc_mrg.rename(
            columns={'VDC_CODE_pc': 'hclit_code_pc', 'DIST_NAME_pc': 'dist_name_pc', 'VDC_NAME_pc': 'vdc_name_pc',
                     'vcode_hh': 'vdc_name_hh', 'mrg_hh': 'vdc_dist_mrg_hh', 'dist': 'dist_hh'})

        return hh_pc_mrg

    def check_hh_pc_cnts(self):
        hh_g = self.hh[['vcode_hh', 'dist_code_hh']].drop_duplicates().groupby('dist_code_hh').count()
        pc_g = self.pcode[['vcode_pc', 'dist_code_pc']].drop_duplicates().groupby('dist_code_pc').count()

        res = pd.merge(hh_g, pc_g, left_index=True, right_index=True, how='left', suffixes=['_hh', '_pc'])
        res['diff'] = res['vcode_hh'] - res['vcode_pc']

        self.log_msg('Diff in counts from CBS data, OCHA pcode:', res)

    def check_cols_str_match(self, df, c1, c2):
        """doesn't return dataset for join, just scores. not working."""
        df['sim'] = df.apply(lambda x: fuzz.partial_ratio(x[c1], x[c2], axis=1))
        self.log_msg('Prox scores below 70:', df[[c1, c2]][df['sim'] < 70])

    def log_msg(self, *strs):
        """nicely log str or set of strs with spaces after"""
        for v in strs:
            logger.info(v)

        logger.info('')
        logger.info('')

d = Dataset()
d.get_nra()