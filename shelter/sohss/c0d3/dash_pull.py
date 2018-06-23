import pandas as pd
import country_converter as coco

"""read in dashboard data, convert ISOz"""


def pull():
    LOC = '../180417 Homepage dashboard data.xlsx'
    hist = pd.read_excel(LOC, sheet_name='DATA FUNDING & BENEFICIARIES')

    # colz
    hist.columns = hist.columns.str.lower()

    hist = hist.rename(
        {'country': 'country',
         'year': 'year',
         'uploaded': 'uploaded',
         'quarter': 'quarter',
         'status': 'status',
         'url': 'url',
         'region': 'region',
         'type of crisis': 'type',
         'lead': 'lead',
         'co-chair / co-lead': 'co_lead',
         'funding received': 'funding_received',
         'funding required': 'funding_required',
         'funding coverage': 'funding_coverage',
         'count': 'count',
         '# of partners': 'num_partner',
         '# of people reached in total': 'num_reached_tot',
         '# of people targeted in total': 'num_targeted_tot',
         'coverage against target': 'cov_against_target',
         '# of people reached with nfi': 'num_reached_nfi',
         '# of people targeted with nfi': 'num_target_nfi',
         '# of people reached with shelter': 'num_reached_shelt',
         '# of people targeted with shelter': 'num_targ_shelt',
         'data from': 'data_from',
         'source/comments': 'source_comment'}, axis=1
    )
    hist.columns = ['dash_' + v for v in hist.columns]

    # drop colz
    hist.drop('dash_unnamed: 20', axis=1, inplace=True)
    hist.drop('dash_coverage against target.1', axis=1, inplace=True)
    hist.drop('dash_unnamed: 24', axis=1, inplace=True)
    hist.drop('dash_coverage against target.2', axis=1, inplace=True)

    # drop rowz
    hist = hist[hist['dash_country'] != 'Pacific Region']

    # new colz (new boyz)
    hist['dash_iso3'] = hist['dash_country'].apply(lambda x: coco.convert(names=x, to='ISO3'))
    hist['dash_uid'] = hist['dash_iso3'] + hist['dash_year'].map(str)

    # rm dupz
    hist = hist.drop_duplicates(subset='dash_uid', keep='last')

    return hist