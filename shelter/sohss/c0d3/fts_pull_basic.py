"""
pulling data from FTS for IFRC GO.

>>Number of CERF Operations and HRPs launched (by type)
>>>count of emergencies by country by year with sum of total funding for funding reuqested vs funding recieved

1) pulls all values from country listing API

2) queryies https://api.hpc.tools/v1/public/fts/flow?countryISO3=XXX&groupby=year for aggreagted yearly
values for funding

3) queries

***coudl have consolidated in one single call without grouping and then done the grouping manually,
        but the grouping is a little complex

run with:
        f = fts(test=True)
        r = f.merge()
        r
"""
import urllib.request, json
import re
import grequests
from itertools import groupby

import pandas as pd
import numpy as np
from pandas.io.json import json_normalize
import dateparser


def api_pull(urls):
    """pull down API contents, and use local history if testing
         urls: list of URLS to pull response from

        results yield the following:
            Sum of incoming flows grouped by the specified source object type
            Sum of incoming flows grouped by the specified destination object type
            ***Sum of incoming and internal flows grouped by the specified destination object type of minus the sum outgoing and internal flows grouped by source objects
            Sum of outgoing flows grouped by destination objects

        we want the ***'d one (report 3)
    """
    if type(urls) != list:
        urls = [urls]

    def exception_handler(request, exception):
        print('Bad URL for ' + str(request))

    print('1st pulling for : ' + str(urls[0]))

    resps = []
    rs = (grequests.get(ref) for ref in urls)
    resps += grequests.map(rs, exception_handler=exception_handler, size=25)

    print('reqs mapped')

    good_resps = []
    bad_resps = []
    for r in resps:
        load = json.loads(r.content)
        load['url'] = r.url
        if r.status_code == 200:
            good_resps.append(load)
        else:
            bad_resps.append(load)

    print('pulled. num bad resps: ' + str(len(bad_resps)))

    return good_resps


class fts(object):
    def __init__(self, test=None):
        self.test = test
        self.cnts = self.get_cnts()

    def get_cnts(self):
        """
        pull down ISO3s from FTS API. here i'm using their provided ISO3s, but we should probably swap in IFRCs
        """

        return [v['iso3'] for v in api_pull('https://api.hpc.tools/v1/public/location')[0]['data']
                if v['iso3'] is not None]

    def get_urls(self, url):
        """
        iterate through cnts to get base URLs for sending to API in bulk
        """
        urls = [url.format(v) for v in self.cnts]

        if self.test:
            return urls[:3]
        else:
            return urls

    def pull_funds(self):
        """
        go through URL list and pull needed info on total, pledged funding and total count
        """
        ret_d = {}

        urls = self.get_urls('https://api.hpc.tools/v1/public/fts/flow?countryISO3={0}&groupby=year')

        for cnt_vals in api_pull(urls):

            # here we pull the ISO from the URL; we could have gotten this at the api_pull, but #yolo (and it'd take some refactoring)
            iso = re.search('ISO3=([A-Z]{3})', cnt_vals['url']).group(1)
            ret_d[iso] = {}

            for fund_area in ['fundingTotals', 'pledgeTotals']:
                if len(cnt_vals['data']['report3'][fund_area]['objects']) > 0:
                    for v in cnt_vals['data']['report3'][fund_area]['objects'][0]['objectsBreakdown']:
                        year = int(v['name'])
                        if year not in ret_d[iso]:
                            ret_d[iso][year] = {fund_area: v['totalFunding']}

                    ret_d[iso][year][fund_area] = v['totalFunding']

        return ret_d

    def pull_evt_cnts(self):
        """
        go through URL list and pull needed info on counts by country and year
        """
        urls = self.get_urls('https://api.hpc.tools/v1/public/emergency/country/{0}')
        ret_d = {}

        for v in api_pull(urls):
            iso = iso = re.search('([A-Z]{3})$', v['url']).group(1)
            assert (iso not in ret_d)
            ret_d[iso] = {}

            # extract years and group by them
            r = json_normalize(v['data']).apply(lambda x: dateparser.parse(x.date).year, axis=1)
            s = r.groupby(r).size()

            for v in s.iteritems():
                # item 0: year, 1: count
                ret_d[iso][v[0]] = v[1]

        return ret_d

    def merge(self):
        """
        join counts and funding amts by building on funds dict
        """
        funds = self.pull_funds()
        cnts = self.pull_evt_cnts()

        # k: country, v: values
        for k, v in cnts.items():
            if k not in funds:
                funds[k] = {}

            # iterate through the dict containing ik:year iv:counts
            for ik, iv in v.items():
                if ik not in funds[k]:
                    funds[k][ik] = {}

                funds[k][ik]['num_activations'] = iv

        return funds

f = fts(test=True)
r = f.merge()
print(r)