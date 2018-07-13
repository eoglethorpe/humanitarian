"""various utils"""
import urllib.request, json

import grequests
import pandas as pd

def api_pull(urls, test = False):
    """pull down API contents, and use local history if testing
        test: boolean, if testing
         urls: list of URLS to pull response from
    """
    def exception_handler(request, exception):
        print('Bad URL for ' + str(request))

    print('pulling for : ' + str(urls[0]))

    resps = []
    rs = (grequests.get(ref) for ref in urls)
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

    print('pulled. num bad resps: ' + str(len(bad_resps)))

    return good_resps