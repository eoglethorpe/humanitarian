"""crawl un info to get all reports"""
import csv
import re
import requests
import os

import grequests
from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive


class infodl(object):

    def __init__(self):
        self.VIEW_BASE = 'http://un.info.np/Net/NeoDocs/View/'
        self.DL_BASE = 'http://un.info.np/System/SignDownloadFile/'
        self.LOGIN = 'http://un.info.np/Shared/Login/'
        self.NUM_DL = 5
        self.FILE_LOC = '/home/ubuntu/code/sand/info/'

    def find_size(self):
        print('find size')
        with open(self.FILE_LOC + 'size.txt', 'wb') as f:
            w = csv.writer(f)

            def exception_handler(request, exception):
                 w.writerow(['broke', request, exception])

            INC = 12
            for i in range(1, self.NUM_DL, INC):
                print('doing ' + str(i))
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
        print ('dl raw')
        b = get_browser()
        b.go(self.LOGIN)

        # posting login form with twill
        fv("1","ctl01$MainContent$Login1$UserName","ewanogle@gmail.com")
        fv("1","ctl01$MainContent$Login1$Password","DOCUMENTS1")

        formaction('1', self.LOGIN)
        b.submit('Sign In')

        # getting binary content with requests using twill cookie jar
        cookies = requests.utils.dict_from_cookiejar(get_browser()._session.cookies)

        with open(self.FILE_LOC + 'type.txt', 'wb') as tf:
            w = csv.writer(tf)

            for i in xrange(self.NUM_DL):
                print('get resp for ' + str(i))
                response = requests.get(self.DL_BASE + str(i), stream=True, cookies=cookies)

                with open(self.FILE_LOC + '%i.txt' % i, 'wb') as handle:
                    row = None
                    if not response.ok:
                        row = [i, 'bad req']
                    else:
                        if 'Content-Disposition' in response.headers:
                            cd = response.headers['Content-Disposition']
                            if cd.startswith('attachment'):
                                row = [i, cd.split('.')[:-1], cd.split('.')[-1]]

                    if not row:
                        row = [i, 'no attach']

                    w.writerow(row)

                    print('write')
                    for block in response.iter_content(61440):
                        handle.write(block)

                response.close()

    def convert(self):
        """iterate through type.txt and convert .txt files based on their names in type.txt"""
        conv = []
        with open(self.FILE_LOC + 'type.txt', 'r') as rf:
            read = csv.reader(rf)

            for row in read:
                if len(row) > 2:
                    os.rename(self.FILE_LOC + '%s.txt' % row[0], self.FILE_LOC + '%s.%s' % (row[0], row[2]))
                    conv.append([row[0], row[2]])
                else:
                    conv.append([row[0], 'no convert'])

        #print conv log
        with open(self.FILE_LOC + 'convert_log.txt', 'wb') as tf:
            w = csv.writer(tf)
            for e in conv:
                w.writerow(e)

    def _find_cnv(self):
        "find out which files should be converted"
        with open(self.FILE_LOC + 'convert_log.txt') as f:
            all = dict(filter(None, csv.reader(f)))

        return [v for v in all.items() if v[1] != 'no convert']

    def mv_drive(self):
        """schlep over to Google drive"""
        FT = 'application/vnd.google-apps.folder'
        FN = 'reports'

        gauth = GoogleAuth()
        gauth.LocalWebserverAuth()
        drive = GoogleDrive(gauth)

        print('checking files')
        file1 = drive.CreateFile()
        fl = drive.ListFile({'q': "'root' in parents and trashed=false"}).GetList()
        print('files checked')

        #create parent folder if not exists
        try:
            id = [k for k in fl if k.metadata['mimeType'] == FT and k.metadata['title'] == FN][0]['id']

        except:
            #if we don't have the folder
            rf = drive.CreateFile({'title': FN,  "mimeType": FT})
            rf.Upload()

            id = [k for k in fl if k.metadata['mimeType'] == FT and k.metadata['title'] == FN][0]['id']
            print('make new reports folder')

        for fn in self._find_cnv():
            dir = '%s/%s.%s' % (self.FILE_LOC, fn[0], fn[1])

            uf = drive.CreateFile({'parents': [{'kind': 'drive#fileLink', 'id': id}], 'title' : fn})
            uf.SetContentFile(os.path.abspath(dir))
            uf.Upload()
            print('title: %s, mimeType: %s' % (uf['title'], uf['mimeType']))

if __name__ == '__main__':
    i = infodl()
    i.mv_drive()