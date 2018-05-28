"""helper tools for ingesting CBS survey data"""

import sqlite3
import sys
import logging

from pandas import DataFrame, read_csv, read_sql
import pandas as pd
import sys
import matplotlib
import numpy as np
import scipy.stats

sys.path.extend(['.', '..'])
import etl

logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)
LOGGER = logging.getLogger(__name__)

def read_hh(loc):
    return pd.read_csv(loc)


def read_pcode(loc):
    return pd.read_csv(loc, encoding='latin-1')

def write_coded_hh(loc):
    pass

def get_dist(dist_codes, dist_in):
    """get district code for a string"""
    try:
        return dist_codes[dist_codes['DIST_NAME'] == dist_in]['DIST_CODE'].values[0]
    except:
        return 'NF'


def get_vdc_digit(vdc_num):
    """ie 5 > 005, 40 > 040"""
    vdc_num = str(vdc_num)
    return '0' * (3 - len(vdc_num)) + vdc_num


def get_12th_poss(pcode):
    """possible values for 12th digits in pcodes...
            5 = normal
            3 = Metropolitan
            9 = Wildlife things
            2 = like 'Sub Metropolitan'
            1 = like 'Kathmandu Metropolitan'
    """

    return {'5': [v[1]['VDC_NAME'] for v in pcode.iterrows() if v[1]['VDC_CODE'][12] == '5'],
            '3': [v[1]['VDC_NAME'] for v in pcode.iterrows() if v[1]['VDC_CODE'][12] == '3'],
            '9': [v[1]['VDC_NAME'] for v in pcode.iterrows() if v[1]['VDC_CODE'][12] == '9'],
            '2': [v[1]['VDC_NAME'] for v in pcode.iterrows() if v[1]['VDC_CODE'][12] == '2'],
            '1': [v[1]['VDC_NAME'] for v in pcode.iterrows() if v[1]['VDC_CODE'][12] == '1']
            }


def get_12th_match(name, poss):
    """get in name, return reccomended 12th digit in based on exact string matching (doesn't really work)"""

    recs = []
    for k, v in poss.items():
        if name in v:
            recs.append(k)

    if len(set(recs)) > 1:
        return 'too many matches for ' + name
    elif len(set(recs)) == 0:
        return 'no matches for ' + name
    else:
        return str(recs[0])


def get_12th_approx(name):
    """return 12th digit based on substring matching"""

    if 'kathmandu metropolitan' in name.lower():
        return '1'
    elif len([True for v in ['sub metropolitan', 'sub-metropolitan'] if v in name.lower()]) >= 1:
        return '2'
    elif 'municipality' in name.lower():
        return '3'
    elif len([True for v in ['park', 'wildlife', 'forest', 'development'] if v in name.lower()]) >= 1:
        return '9'
    else:
        return '5'

def check_dist_mispelled(hh, dist_codes):
    LOGGER.info('Mispelled districts:')

    for v in hh['dist'].drop_duplicates():
        if v not in dist_codes['DIST_NAME'].values:
            LOGGER.info(v)


def check_hh_all_dist_ok(hh):
    LOGGER.info('Unassigned districts in HH:')
    LOGGER.info(hh[hh['DIST_NAME'].isnull()]['dist'].drop_duplicates())


def fix_mispelled_dists(hh, dist_codes):
    """fix mispelled district names in HH data"""

    #replace L in hh with R
    rep = {'Sankhuwasabha' : 'Sangkhuwasabha',
         'Chitwan' : 'Chitawan',
         'Kavrepalanchok' : 'Kabhrepalanchok',
         'Makwanpur' : 'Makawanpur',
         'Tanahu' : 'Tanahun'}

    for org, new in rep.items():
        hh.loc[hh['dist'] == org, 'dist'] = new

    return hh


def add_dist_codes(hh, pcode):
    """add in column for district codes, fix spelling errors"""
    LOGGER.info('Adding district codes')
    dist_codes = pcode.loc[:, ['DIST_CODE', 'DIST_NAME']].drop_duplicates()

    check_dist_mispelled(hh, dist_codes)

    hh = fix_mispelled_dists(hh, dist_codes)

    LOGGER.info('Fixed district mispellings, checking again:')
    check_dist_mispelled(hh, dist_codes)

    #join hh data with dist codes
    hh = pd.merge(hh, dist_codes, left_on='dist', right_on='DIST_NAME', how='left')
    check_hh_all_dist_ok(hh)

    hh = hh.drop('DIST_NAME', axis=1)
    hh = hh.rename(columns={'DIST_CODE': 'dist_code'})

    return hh


def add_vdc_codes(hh):
    """add in vdc code. first we make a temporary table with unique vdc values and then join the results,
        this is much faster than doing the apply function for each entry"""
    LOGGER.info('Adding VDC codes')
    tmp = hh.loc[:, ['vdcmun', 'vcode', 'dist_code']].drop_duplicates()
    tmp['full_vdc'] = tmp.apply(lambda x: '{0} {1} {2}'.format(x['dist_code'],
                                                               str(get_12th_approx(x['vcode'])),
                                                               get_vdc_digit(x['vdcmun'])), axis=1)

    return pd.merge(hh, tmp, left_on=['dist_code', 'vdcmun'], right_on=['dist_code', 'vdcmun'], how='left')\
        .drop(['vcode_y'], axis = 1)\
        .rename(columns = {'vcode_x' : 'vdc_nm', 'full_vdc' : 'vdc_code'})


def get_coded_cbs_hh():
    """return cbs hh data with vdc and district codes"""
    LOGGER.info('Importing...')
    hh = read_hh('../data/' + etl.HH_NAME)
    pcode = read_pcode('../data/' + etl.PCODE_NAME)
    # poss = get_12th_poss(pcode)

    return add_vdc_codes(add_dist_codes(hh, pcode))