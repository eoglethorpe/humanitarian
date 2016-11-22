"""crawl un info to get all reports"""
import csv
import re
import requests

import grequests
from twill.commands import *

class infodl(object):

    def __init__(self):
        self.VIEW_BASE = 'http://un.info.np/Net/NeoDocs/View/'
        self.DL_BASE = 'http://un.info.np/System/SignDownloadFile/'
        self.LOGIN = 'http://un.info.np/Shared/Login/'
        self.NUM_DL = 5

    def find_size(self):
        with open('/tmp/size.txt', 'wb') as f:
            w = csv.writer(f)

            def exception_handler(request, exception):
                 w.writerow(['broke', request, exception])

            INC = 12
            for i in xrange(1, self.NUM_DL, INC):
                print 'doing ' + str(i)
                rs = (grequests.get(self.BASE + str(x)) for x in xrange( i, i+INC))
                resps = grequests.map(rs, exception_handler = exception_handler)

                for smalli, req in enumerate(resps):
                    if req.text.rfind('Invalid Operation !\r\n') == -1:
                        #this is a valid link
                        r = re.search('<span id="ctl01_MainContent_view1_LabelFileSize">(.*?)\</span>', req.text)
                        if r:
                            sz = r.group(1).split(' ')
                            w.writerow(['size', i + smalli, sz[0], sz[1]])
                        else:
                            w.writerow(['size', i + smalli, 'notfound'])

                    else:
                        w.writerow(['nolink', i + smalli])

    def dl_raw(self):
        b = get_browser()
        b.go(self.LOGIN)

        # posting login form with twill
        fv("1","ctl01$MainContent$Login1$UserName","")
        fv("1","ctl01$MainContent$Login1$Password","")

        formaction('1', self.LOGIN)
        b.submit('Sign In')

        # getting binary content with requests using twill cookie jar
        cookies = requests.utils.dict_from_cookiejar(get_browser()._session.cookies)

        with open('/tmp/files/type.txt', 'wb') as tf:
            for i in xrange(self.NUM_DL):
                response = requests.get(url, stream=True, cookies=cookies)

                with open('/tmp/files/%i.txt' % i, 'wb') as handle:
                    if not response.ok:
                        tf.writerow([i, 'bad req'])
                    else:
                        tf.writerow([i, response.headers['Content-Type']])

                    print 'write'
                    for block in response.iter_content(10240):
                        handle.write(block)


if __name__ == '__main__':
    i = infodl()
        i.dl_raw()