"""for pulling down data from hr.info API on response level and sending to CSV"""
#locations: https://api.hpc.tools/v1/public/location
#clusters: https://api.hpc.tools/v1/public/global-cluster ["code":"SHL"]
#https://api.hpc.tools/docs/v1/
#boundary cat by looping through locations

#TODO: subtract outgoing

import urllib.request, json
import csv
import itertools
import math
import collections
import sys

import grequests
import pandas as pd
import numpy as np
from pandas.io.json import json_normalize

class fts(object):
    def __init__(self, sc, test=None, all_sector=False):
        self.all_sector = all_sector
        self.test = test
        self.sc = sc

        self.fts = self.master_pull()
        self.merge_sc()
        self.flows = self.extract_flows()

        # remove flows col as it's quite large
        self.fts = self.fts.drop('fts.data.flows', axis=1)

    def extract_flows(self):
        """take all flows and add to df"""

        flow_df = pd.DataFrame()
        for v in self.fts.iterrows():
            norm = json_normalize(v[1]['fts.data.flows'])
            norm['fts.uid'] = v[1]['fts.uid']

            if len(flow_df) == 0:
                flow_df = norm
            else:
                # need to make sure we're adding t3h same c0lz
                assert (norm.columns.all(flow_df.columns))
                flow_df = flow_df.append(norm, ignore_index=True)

        return flow_df

    def master_pull(self):
        """group by year, country and pull down total values with optional filter by cluster"""
        countries = json_normalize(json.loads(urllib.request.urlopen("https://api.hpc.tools/v1/public/location")
                                              .read().decode()))['data']

        print('pulled countries')

        self.hist = self.sc

        self.hist['sc.fts_url'] = self.hist.apply(lambda x: \
                                                      'https://api.hpc.tools/v1/public/fts/flow?countryISO3={0}&year={1}{2}' \
                                                  .format(x['sc.iso3'], x['sc.year'], \
                                                          '&globalClusterCode=shl' if not self.all_sector else ''),
                                                  axis=1)

        if self.test:
            hrefz = self.hist['sc.fts_url'][:self.test]
        else:
            hrefz = self.hist['sc.fts_url']

        def exception_handler(request, exception):
            print('Bad URL for ' + request)

        resps = []
        rs = (grequests.get(ref) for ref in hrefz)
        resps += grequests.map(rs, exception_handler=exception_handler, size=25)

        good_resps = []
        bad_resps = []
        for r in resps:
            load = json.loads(r.content)
            load['url'] = r.url
            if r.status_code == 200:
                good_resps.append(load)
            else:
                bad_resps.append(load)

        print('num bad resps: ' + str(len(bad_resps)))
        return json_normalize(good_resps).add_prefix('fts.')

    def merge_sc(self):
        self.fts = self.fts.merge(self.hist, left_on='fts.url', right_on='sc.fts_url')

    def get_flow_bdown(self):
        def hp(v):
            if 'Plan' in json_normalize(v['destinationObjects']).values or 'Plan' in json_normalize(
                    v['sourceObjects']).values:
                return 'has_plan'
            else:
                return 'no_plan'

        self.flows['plan'] = self.flows.apply(lambda x: hp(x), axis=1)

        # we are skipping boundary for now as it's <<<<
        d = self.flows[['fts.uid', 'plan', 'amountUSD']].groupby(['fts.uid', 'plan'], as_index=False).aggregate(
            {'amountUSD': 'sum'})
        piv = pd.pivot_table(d, index='fts.uid', values='amountUSD', aggfunc=np.sum, columns=[d['plan']] \
                             , fill_value=0).reset_index()
        piv['total'] = piv['has_plan'] + piv['no_plan']
        return piv

