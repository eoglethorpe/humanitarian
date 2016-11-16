"""crawl un info to get all reports"""
from lxml import html
import grequests


def find_count():
    br = 0
    gd = 0
    bd = 0

    BASE = 'http://un.info.np/Net/NeoDocs/View/'
    rs = (grequests.get(BASE + str(i)) for i in xrange(5000))
    reqs = grequests.map(rs)

    def exception_handler(request, exception):
        global br
        br +=1

    for req in reqs:
        if req.text.rfind('Invalid Operation !\r\n') == -1:
            gd += 1
        else:
            bd += 1

    print 'bad: ' + str(bd)
    print 'good: ' + str(gd)
    print 'broken: ' + str(br)
    print

if __name__ == '__main__':
    find_count()