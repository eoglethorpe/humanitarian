import pandas as pd
import country_converter as coco

"""read in SC historical data, convert ISOz"""


def pull():
    LOC = '../d0cz/sc_historical.xlsx'
    hist = pd.read_excel(LOC, sheet_name='Sheet2')

    # fix columns
    if 'Unnamed: 12' in hist.columns:
        hist = hist.drop('Unnamed: 12', axis=1)

    hist = hist.rename(columns =
        {
            'Region' : 'region',
            'Region URL' : 'region_url',
            'Country ' : 'country',
            'Country URL' : 'country_url',
            'Year' : 'year',
            'Response' : 'response',
            'Lead Agency' : 'lead_agency',
            'Disaster type' : 'disaster_type',
            'Website URL' : 'website_url',
            'Co-Lead Agency' : 'colead_agency',
            'Activation date' : 'activation_date',
            'Deactivation date' : 'deactivation_date',
            'num_clust' : 'num_clust'
         })

    # Pacific Region given for 2015 - 2018, remove
    hist = hist[hist['country'] != 'Pacific Region']

    # Rename 'Chili' to 'Chile'
    hist.loc[hist['country'] == 'Chili', 'country'] = 'Chile'

    # add ISO codes
    hist['iso3'] = hist['country'].apply(lambda x: coco.convert(names=x, to='ISO3'))

    #add UID column
    hist['uid'] = hist['iso3'] + hist['year'].astype(str)

    #check to see if there are duplicates
    assert(True not in list(hist['uid'].duplicated()))
    # print(list(hist['uid'].duplicated()))

    # total number of crisis: 230
    print('loaded ' + str(len(hist)) + ' SC entries')

    #prepend prefix
    hist.columns = ['sc.' + v for v in hist.columns]

    return hist