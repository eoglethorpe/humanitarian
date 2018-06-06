"""for pulling down data from hr.info API on response level and sending to CSV"""
#locations: https://api.hpc.tools/v1/public/location
#clusters: https://api.hpc.tools/v1/public/global-cluster ["code":"SHL"]
#https://api.hpc.tools/docs/v1/
#boundary cat by looping through locations

import urllib.request, json
import csv
import itertools
import math
import collections

import grequests
import pandas as pd
from pandas.io.json import json_normalize

def pull(sc):
    """group by year, country and pull down total values with optional filter by cluster.
        requires SC base data
    """
    countries = json_normalize(json.loads(urllib.request.urlopen("https://api.hpc.tools/v1/public/location")
                                          .read().decode()))['data']

    print('pulled countries')

    sc['fts_url'] = sc.apply(lambda x : 'https://api.hpc.tools/v1/public/fts/flow?countryISO3={0}&year={1}&globalClusterCode=shl'
                                 .format(x['ISO3'], x['Year']), axis = 1)

    hrefz = sc['fts_url']

    def exception_handler(request, exception):
         print('Bad URL for ' + request)

    resps = []
    rs = (grequests.get(ref) for ref in hrefz)
    resps += grequests.map(rs, exception_handler = exception_handler, size = 25)

    good_resps = []
    bad_resps = []
    for r in resps:
        if r.status_code == 200:
            good_resps.append(json.loads(r.content))
        else:
            bad_resps.append(json.loads(r.content))


    j = json_normalize(good_resps).add_prefix('fts.')