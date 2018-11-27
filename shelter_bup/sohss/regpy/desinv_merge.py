import json
import pandas as pd

countries = [
    'COD', 'PAK', 'IDN', 'LBN', 'LBR', 'PHL', 'SOM', 'UGA', 'BGD', 'CAF',
    'TCD', 'ETH', 'MOZ', 'AFG', 'GEO', 'HTI', 'IRQ', 'KEN', 'MMR', 'NPL',
    'SDN', 'TJK', 'YEM', 'BFA', 'SLV', 'Sri', 'LKA', 'BEN', 'CHL', 'KGZ',
    'CIV', 'LSO', 'LBY', 'COL', 'FJI', 'MLI', 'PER', 'SSD', 'PSE', 'PRY',
    'SLB', 'SYR', 'UKR', 'MWI', 'VUT', 'NGA', 'ECU', 'MDG', 'TON'
]

all = None
# cols = OrderedDict()
base_cols = ['Year','Deaths','Injured','Missing','Houses Destroyed','Houses Damaged','Relocated','Evacuated','Losses $USD']

countrycodes = {}

with open('countries.json') as f:
    countrycodes = json.loads(f.read())

for c in countries:
    code = c.lower()
    try:
        df = pd.read_csv('downloaded_xls/{}.xls'.format(code), sep='\t')
    except Exception as e:
        print('error', e)
    else:
        cols = df.columns
        renamed = {x: x.strip() for x in cols}
        df = df.rename(index=str, columns=renamed)
        df = df.filter(items=[*base_cols])
        df['Country Code'] = [code.upper() for _ in df['Deaths']]
        df['Country'] = [countrycodes.get(code.upper(), code) for _ in df['Deaths']]
        df = df.reindex_axis(['Country Code', 'Country'] + base_cols, axis=1)
        df = df.drop(df[df['Year'] < '2005'].index)
        df = df.drop(df[df['Year'] == 'TOTAL'].index)

        if all is None:
            all = df.copy()
        else:
            all = pd.concat([all, df])

all.to_csv('countries_data.csv')

