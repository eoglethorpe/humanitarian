import pandas as pd

from fts_pull import fts
from rw_pull import rw
import sc_pull
import desinv_pull
import dash_pull

sc = sc_pull.pull()

def get_rw():
    r = rw(test = (10,20), year = 2005, sc = sc)
    r = r.master_pull()

    rw_cnt = pd.DataFrame(r['rw.uid'].value_counts()).reset_index()
    rw_cnt.columns = ['rw.uid', 'rw.cnt']

    return rw_cnt

def get_fts():
    all_f = fts(sc = sc, test = 10, all_sector=True)
    s_f = fts(test = 10, sc = sc)

    all_b = all_f.get_flow_bdown()
    all_b.rename({'total': 'all_total'}, inplace=True, axis=1)

    sf_b = s_f.get_flow_bdown()
    sf_b.rename({'total': 'sc_total'}, inplace=True, axis=1)

    mrgd = sf_b.merge(all_b[['fts.uid', 'all_total']], left_on='fts.uid', right_on='fts.uid', how='left')
    mrgd['all_total'] = mrgd['all_total'] - mrgd['sc_total']

    return mrgd

def get_desinv():
    return desinv_pull.pull()

def get_dash():
    return dash_pull.pull()

#get dataz
rw = get_rw()
fts = get_fts()
div = get_desinv()
dash = get_dash()

merge_d = { 'rw' : 'rw.uid',
            'fts' : 'fts.uid',
            'div': 'div_uid',
            'dash' : 'dash_uid'
        }

#merge
for k,v in merge_d.items():
    sc = sc.merge(globals()[k], left_on='sc.uid', right_on=v, how='left')

#drop
for v in merge_d.values():
    sc.drop(v, axis=1, inplace=True)

sc.to_csv('../d0cz/out.csv')

# #merge rw
#
#
# #merge fts
# sc = sc.merge(fts, left_on = 'sc.uid', right_on = 'fts.uid', how = 'left')
#
# #merge div
# sc = sc.merge(div, left_on = 'sc.uid', right_on = 'div_uid', how = 'left')
#
# merge dash


# #drop cols
#
# sc.drop('fts.uid', axis = 1)
# sc.drop('div_uid', axis = 1)

