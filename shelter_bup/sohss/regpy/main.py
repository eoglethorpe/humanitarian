from fts_pull import fts
from rw_pull import rw
import sc_pull
import desinv_pull

import pandas as pd

sc = sc_pull.pull()

def get_rw():
    r = rw(test = None, year = 2005, sc = sc)
    return r.master_pull()

def get_fts():
    all_f = fts(sc = sc, all_sector=True)
    s_f = fts(sc = sc)

    all_b = all_f.get_flow_bdown()
    all_b.rename({'total': 'all_total'}, inplace=True, axis=1)

    sf_b = s_f.get_flow_bdown()
    sf_b.rename({'total': 'sc_total'}, inplace=True, axis=1)

    mrgd = sf_b.merge(all_b[['sc.uid', 'all_total']], how='left', on='sc.uid')
    mrgd['all_total'] = mrgd['all_total'] - mrgd['sc_total']

    return mrgd

#get dataz
rw = get_rw()
fts = get_fts()
div = desinv_pull.pull()

#merge rw
rw_cnt = pd.DataFrame(rw['rw.uid'].value_counts()).reset_index()
rw_cnt.columns = ['rw.uid', 'rw.cnt']
sc = sc.merge(rw_cnt, left_on = 'sc.uid', right_on = 'rw.uid', how = 'left')

#merge fts
sc = sc.merge(fts, left_on = 'sc.uid', right_on = 'fts_fts.uid', how = 'left')

#merge div
sc = sc.merge(div, left_on = 'sc.uid', right_on = 'div_uid', how = 'left')

#drop cols
sc.drop('rw.uid', axis = 1)
sc.drop('fts_fts.uid', axis = 1)
sc.drop('div_uid', axis = 1)