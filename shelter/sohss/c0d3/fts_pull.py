"""for pulling down data from hr.info API on response level and sending to CSV"""
#locations: https://api.hpc.tools/v1/public/location
#clusters: https://api.hpc.tools/v1/public/global-cluster ["code":"SHL"]
#https://api.hpc.tools/docs/v1/
#boundary cat by looping through locations

#TODO: subtract outgoing

import urllib.request, json
import re
from itertools import groupby

import pandas as pd
import numpy as np
from pandas.io.json import json_normalize

import utils


class fts(object):
    def __init__(self, sc, test=None, all_sector=False):
        self.all_sector = all_sector
        self.test = test
        self.sc = sc

        self.fts = self.master_pull()
        # self.merge_sc()
        self.flows = self.extract_flows()

        # remove flows col as it's quite large
#         self.fts = self.fts.drop('fts.data.flows', axis=1)

    def master_pull(self):
        """group by year, country and pull down total values with optional filter by cluster.
            returns: dict of {sector 1 : info df}
        """
        SHELTER_ABBRV = 'SHL'

        if self.test:
            self.hist = self.sc[:self.test]
        else:
            self.hist = self.sc

        #create cluster_vals which will be a dict of {cluster : df}
        """
            AGR : Agriculture
            CCM : Camp Coordination / Management
            PRO-CPN : Child Protection
            CSS : Coordination and support services
            ERY : Early Recovery
            EDU : Education
            SHL : Emergency Shelter and NFI
            TEL : Emergency Telecommunications
            FSC : Food Security
            PRO-GBV : Gender Based Violence
            HEA : Health
            PRO-HLP : Housing, Land and Property
            LOG : Logistics
            PRO-MIN : Mine Action
            MS : Multi-sector
            NUT : Nutrition
            OTH : Other
            PRO : Protection
            WSH : Water Sanitation Hygiene
        """
        clusters = [SHELTER_ABBRV]
        if self.all_sector:
            clusters = [v['code'] for v in json_normalize(json.loads \
                                                              (urllib.request.urlopen(
                                                                "https://api.hpc.tools/v1/public/global-cluster")
                                                                .read().decode()))['data'][0]]

        #for each cluster, prep string for each URL and get year
        URL_STR = 'https://api.hpc.tools/v1/public/fts/flow?countryISO3={0}&year={1} &globalClusterCode={2}'
        hrefz = []
        for clust in clusters:
            self.hist.apply(lambda v: hrefz.append(URL_STR.format(v['sc.iso3'], v['sc.year'], clust)) , axis = 1)

        # now submit the URLs to the API service and concat together and
        # then assign to cluster_values using cluser code in URL
        pulled = None
        for v in utils.api_pull(hrefz, False):
            ins_df = json_normalize(v['data'])

            ins_df['sector'] = re.match('.*globalClusterCode=(.*)', v['url']).groups()[0]
            ins_df['year'] = re.match('.*year=([0-9]{4})', v['url']).groups()[0]
            ins_df['iso3'] = re.match('.*countryISO3=(.{3})', v['url']).groups()[0]

            if pulled is None:
                pulled = ins_df

            else:
                pulled = pd.concat([pulled, ins_df])

        return pulled.add_prefix('fts.')

    def merge_sc(self):
        self.fts = self.fts.merge(self.hist, left_on='fts.url', right_on='sc.fts_url')

    def extract_flows(self):
        """take all flows and add to df"""

        flow_df = pd.DataFrame()
        for v in self.fts.iterrows():
            norm = json_normalize(v[1]['fts.flows'])
            norm['fts.uid'] = v[1]['fts.iso3'] + v[1]['fts.year']
            norm['fts.sector'] = v[1]['fts.sector']

            if len(flow_df) == 0:
                flow_df = norm

            else:
                # need to make sure we're adding t3h same c0lz
                assert (norm.columns.all(flow_df.columns))
                flow_df = flow_df.append(norm, ignore_index=True)

        return flow_df

    def get_flow_bdown(self):
        """break down flows by needed columns"""

        def hp(v):
            if 'Plan' in json_normalize(v['destinationObjects']).values or 'Plan' in json_normalize(
                    v['sourceObjects']).values:
                return 'sc_has_plan'
            else:
                return 'sc_no_plan'

        #not graceful, should be better
        self.flows['plan'] = self.flows.apply(lambda x: hp(x), axis=1)

<<<<<<< HEAD
        # we are skipping boundary for now as it's <<<<
=======
>>>>>>> ff48016fea7cc982fe07ae5b4a525a8a4249c189
        d = self.flows[['fts.uid', 'fts.sector', 'amountUSD']].groupby(['fts.uid', 'fts.sector'], as_index=False).aggregate(
            {'amountUSD': 'sum'})
        piv = pd.pivot_table(d, index='fts.uid', values='amountUSD', aggfunc=np.sum, columns=[d['fts.sector']] \
                             , fill_value=0).reset_index()

        #do shelter plan/no plan
        s_d = self.flows[['fts.uid', 'amountUSD', 'plan']].loc[self.flows['fts.sector'] == 'SHL']\
                                .groupby(['fts.uid', 'plan'], as_index=False).aggregate(
                                {'amountUSD': 'sum'})
        s_piv = pd.pivot_table(s_d, index='fts.uid', values='amountUSD', aggfunc=np.sum, columns=[s_d['plan']] \
                             , fill_value=0).reset_index()

        mrgd = piv.merge(s_piv, on = 'fts.uid', how = 'outer')

        mrgd.columns = ['fts.' + v.lower() if 'fts.' not in v else v.lower() for v in mrgd.columns]

        return mrgd


import sc_pull
sc = sc_pull.pull()
# s_f = fts(test=2, sc=sc)
all_f = fts(sc=sc, all_sector=True)
all_f.get_flow_bdown().to_csv('../d0cz/fts_out.csv')
#
# print(s_f.get_flow_bdown().add_prefix('sc_')) #351513201 PAK2005 sc
# # print(all_f.get_flow_bdown().add_prefix('sc_')) #351513201 PAK2005 all
#
# # AGR,CCM,PRO-CPN,CSS,ERY,EDU,TEL,FSC,PRO-GBV,HEA,PRO-HLP,LOG,PRO-MIN,MS,NUT,OTH,PRO,WSH
