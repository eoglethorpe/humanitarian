"""crawl un info to get all reports"""
from lxml import html
import requests


def find_count():
    base= 'http://un.info.np/Net/NeoDocs/View/'

    good = 0
    bad = 0
    for i in xrange(8000):
        cur = base + str(i)
        req = requests.get(cur)
        if req.text.rfind('Invalid Operation !\r\n') == -1:
            bad += 1
        else:
            good += 1

        print 'bad: ' + str(bad)
        print 'good: ' + str(good)
        print
        break

if __name__ == '__main__':
    find_count()