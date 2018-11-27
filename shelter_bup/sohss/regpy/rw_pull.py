import urllib.request, json
import csv
import itertools
import math

import grequests
import pandas as pd
from pandas.io.json import json_normalize

def pull_indiv_rw(data):
    """
    return all individual crisis data, exclude ones that don't have a 200 status code.

    pull into a df and return, then that gets merged with the existing df
    """
    hrefz = data['rw_gen.href']

    def exception_handler(request, exception):
        print('Bad URL for ' + request)

    resps = []
    it = 200
    for v in range(0, len(hrefz), it):
        print('Pulling individual for hrefs to ' + str(v))
        rs = (grequests.get(ref) for ref in hrefz[v: v + it])
        resps += grequests.map(rs, exception_handler=exception_handler)

    resps = [json.loads(r.content) for r in resps if r.status_code == 200]

    return json_normalize(resps)[['data', 'href', 'totalCount']].add_prefix('rw_gen.')

def fetch_api_rw(maxv=None):
    """
    pull down all API info for RW general crisis and return as dataframe.

    maxv = (start_val, end_val)
    """
    data = []

    if maxv:
        start = maxv[0]
        fin = maxv[1]
        step = min(fin - start, 1000)

    else:
        start = 0
        fin = json.loads(urllib.request.urlopen("https://api.reliefweb.int/v1/" \
                                                "disasters?appname=vocabulary&preset=external").read().decode())[
            'totalCount']
        step = 1000

    for i in range(start, fin, step):
        with urllib.request.urlopen("https://api.reliefweb.int/v1/disasters?appname=vocabulary"
                                    "&preset=external&limit={0}&offset={1}"
                                            .format(min(step, fin - i), i)) as url:
            data += json.loads(url.read().decode())['data']

    ret = json_normalize(data).add_prefix('rw_gen.')

    assert (len(ret) == fin - start)
    print('pulling down from rw entry count of: ' + str(len(ret)))
    return ret


class rw(object):
    def t(self):
        pass

    def __init__(self, test, year, sc):
        self.test = test
        self.data = None
        self.year = year
        self.sc = sc

    def extract_date(self, val):
        name = val.replace(' ', '')[-7:]
        month = None
        year = None

        MIN_YEAR = 2005
        # if we don't have regular formatting, take just year
        if not name[0:3].isalpha():
            if not name[-4:].isnumeric():
                print("***bad year: " + name)
            else:
                year = int(name[-4:])
        else:
            month = name[:3]
            year = int(name[-4:])

        if year:
            if year >= MIN_YEAR:
                return [month, year]

        return (None, None)

    def get_date(self):
        self.data['rw_gen.month'] = None
        self.data['rw_gen.year'] = None
        self.data[['rw_gen.month', 'rw_gen.year']] = self.data.apply(lambda x:
                                                                     pd.Series(
                                                                         self.extract_date(x['rw_gen.fields.name'])),
                                                                     axis=1)

        self.data = self.data[pd.notnull(self.data['rw_gen.year'])]
        self.data['rw_gen.year'] = self.data['rw_gen.year'].astype(int)

    def trim_nm(self):

        def trim(v):
            s_val = None

            if len(v.split('-')) != 1:
                s_val = '-'
            elif len(v.split('–')) != 1:
                s_val = '–'

            if s_val:
                return v.split(s_val)[0]
            else:
                return v

        self.data['rw_gen.fields.name'] = self.data.apply(lambda x: trim(x['rw_gen.fields.name']), axis=1)

    def rm_old(self):
        self.data = self.data.drop(self.data[self.data['rw_gen.year'] < self.year].index)
        print('trim data length: ' + str(len(self.data)))

    def _get_spec_crisis_lamb(self, v):
        ret = []

        if v['rw_gen.totalCount'] != 1:
            print('***wrong totalCount ' + str(v))

        j = json_normalize(v['rw_gen.data'][0])

        # add in top level data compents
        try:
            ret += [j[ent.split('data.')[1]][0] for ent in self.new_cols_top]

        except:
            ret += [None] * len(self.new_cols_top)

        # add in data.fields info. entry be like:
        """
            {'href': 'https://api.reliefweb.int/v1/countries/255',
             'id': 255,
             'iso3': 'yem',
             'location': {'lat': 15.94, 'lon': 47.62},
             'name': 'Yemen',
             'primary': True}
            primary = None
        """

        # add in other columns
        for v in j['fields.country'][0]:
            if 'primary' in v:
                primary = v
                break

                # bad news if no primary
        if not primary:
            print('*** no primary! ' + str(v))
            ret = [None] * (len(self.all_cols) - len(self.new_cols_top))

        else:
            try:
                rollback = ret

                # also add in other cols
                ret.append(len(j['fields.country'][0]))

                ret += [primary[c] for c in ['name', 'iso3', 'href']]
                ret.append(primary['location']['lat'])
                ret.append(primary['location']['lon'])

            except:
                ret = rollback + [None] * (len(rollback) - (len(self.all_cols) - len(self.new_cols_top)))

        return ret

    def get_spec_crisis(self):
        """
        merge relevant crisis level data
        """

        l = pull_indiv_rw(self.data)

        l['rw_gen.totalCount'] = l['rw_gen.totalCount'].astype(int)

        self.new_cols_top = ['data.fields.description',
                             'data.fields.url_alias']

        self.other_cols = ['num_country']

        self.new_cols_country = ['data.fields.country.name',
                                 'data.fields.country.iso',
                                 'data.fields.country.href',
                                 'data.fields.country.location_lat',
                                 'data.fields.country.location_long']

        self.all_cols = self.new_cols_top + self.other_cols + self.new_cols_country

        for v in self.all_cols:
            l[v] = None

        l[self.all_cols] = l.apply(lambda x: pd.Series(self._get_spec_crisis_lamb(x)), axis=1)

        # drop unnecessary columns, cleanup
        l = l.drop('rw_gen.data', axis=1)
        l = l.drop('rw_gen.totalCount', axis=1)
        l['num_country'] = l['num_country'].astype(int)

        self.data = self.data.merge(l, how='left', on='rw_gen.href')

    def add_uid(self):
        self.data['rw.uid'] = self.data['data.fields.country.iso'].str.upper() + self.data['rw_gen.year'].map(str)

    def check_in_sc(self):
        self.data['rw.in_sc'] = self.data['rw.uid'].isin(self.sc['sc.uid'])

    def master_pull(self):
        """take crises only after certain year, add month_crisis: mmm, and year_crisis: yyyy to each crisis's entry

            names are either in format of:
                MMM YYYY
                OR
                YYYY-YYYY

            if not in first format, check to see if end year > 2005
        """
        # only pull some data if test
        if self.test:
            self.data = fetch_api_rw(self.test)
        else:
            self.data = fetch_api_rw()

        # do things to primary rw data
        self.get_date()
        self.rm_old()
        self.trim_nm()

        # do crisiswise pull
        self.get_spec_crisis()

        #sc, uid
        self.add_uid()
        self.check_in_sc()

        return self.data