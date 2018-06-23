"""read in HCR data, convert ISOz... output total counts a country's incoming and outgoing
    """
from collections import OrderedDict
import logging

import pandas as pd
import country_converter as coco
import numpy as np

pd.options.display.max_rows = 999

logger = logging.getLogger('log')
logger.setLevel(logging.CRITICAL)


class hcr(object):
    def __init__(self):
        self.base = self.pull_base()

    def clean_col(self, val):
        try:
            return int(val)
        except:
            return np.NaN

    def group(self, key, iso, prefix):
        """group either incoming or outgoing"""
        self.base[key] = self.base[iso].map(str) + self.base['ref_year'].map(str)

        out_vals = ['ref_refugees', 'ref_asylum-seekers', 'ref_returned_refugees', 'ref_idps', 'ref_returned_idps',
                    'ref_stateless_persons', 'ref_others_of_concern', 'ref_total_population']

        gpd = self.base[[key] + out_vals] \
            .groupby(key, as_index=False).sum()

        piv = pd.pivot_table(gpd, index=key, values=out_vals, aggfunc=np.sum).reset_index()

        for v in out_vals:
            piv[v] = piv[v].astype(int)

        return piv.add_prefix(prefix)

    def pull_base(self):
        """
            get the base table for incoming/outgoing movements, and then use it to generate the other 2 tables
        """
        LOC = '../d0cz/unhcr_popstats_export_persons_of_concern_2018_06_20.csv'
        ref = pd.read_csv(LOC, skiprows=3)
        ref.columns = ['ref_' + v.lower().strip().replace(' ', '_') for v in ref.columns.values]

        # only rename weird cols, keep the rest. total:
        """
        ref_year
        ref_destination
        ref_origin
        ref_refugees
        ref_asylum-seekers
        ref_returned_refugees
        ref_idps
        ref_returned_idps
        ref_stateless_persons
        ref_others_of_concern
        ref_total_population
        """
        ref.rename(
            {
                'ref_country_/_territory_of_asylum/residence': 'ref_destination',
                'ref_refugees_(incl._refugee-like_situations)': 'ref_refugees',
                'ref_asylum-seekers_(pending_cases)': 'ref_asylum-seekers',
                'ref_internally_displaced_persons_(idps)': 'ref_idps'}, axis=1, inplace=True)

        # add in ISOs, uid
        trans = {v: coco.convert(names=v, to='ISO3') \
                 for v in list(set(list(ref.ref_destination.values) + list(ref.ref_origin.values)))}
        trans['Serbia and Kosovo (S/RES/1244 (1999))'] = 'SRB'
        trans['Tibetan'] = 'CHN'

        ref['ref_dest_iso3'] = ref.apply(lambda x: trans[x['ref_destination']], axis=1)
        ref['ref_org_iso3'] = ref.apply(lambda x: trans[x['ref_origin']], axis=1)
        assert (list not in [type(v) for v in trans.values()])

        # clean cols
        tc = ['ref_refugees', 'ref_asylum-seekers', 'ref_returned_refugees', 'ref_idps', 'ref_returned_idps',
              'ref_stateless_persons', 'ref_others_of_concern', 'ref_total_population']

        for c in tc:
            ref[c] = ref.apply(lambda x: self.clean_col(x[c]), axis=1)

        return ref