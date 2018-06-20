import requests
import pandas as pd
from bs4 import BeautifulSoup as Soup


countries = [
    'COD', 'PAK', 'IDN', 'LBN', 'LBR', 'PHL', 'SOM', 'UGA', 'BGD', 'CAF',
    'TCD', 'ETH', 'MOZ', 'AFG', 'GEO', 'HTI', 'IRQ', 'KEN', 'MMR', 'NPL',
    'SDN', 'TJK', 'YEM', 'BFA', 'SLV', 'Sri', 'LKA', 'BEN', 'CHL', 'KGZ',
    'CIV', 'LSO', 'LBY', 'COL', 'FJI', 'MLI', 'PER', 'SSD', 'PSE', 'PRY',
    'SLB', 'SYR', 'UKR', 'MWI', 'VUT', 'NGA', 'ECU', 'MDG', 'TON'
]

HEADERS = {
    'Host': 'www.desinventar.net',
    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:60.0) Gecko/20100101 Firefox/60.0',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    'Accept-Language': 'en-US,en;q=0.5',
    'Accept-Encoding': 'gzip, deflate, br',
    'Referer': 'https://www.desinventar.net/DesInventar/profiletab.jsp?countrycode={}&continue=y',
    'Content-Type': 'application/x-www-form-urlencoded',
    'Cookie': 'JSESSIONID=9C2A28DD2E26924CC49E97BF05258DDD',
    'Connection': 'keep-alive',
    'Upgrade-Insecure-Requests': '1'
}

DEFINESTATS_BODY = {
    'eventos': '',
    'level0': '',
    'name0': '',
    'actiontab': 'definestats.jsp',
    'frompage': '%2Fprofiletab.jsp'
}
STATISTICS_POST_BODY = {
    'actiontab': 'statistics.jsp',
    'bSum': 'Y',
    'continue': 'Continue',
    'frompage': '/definestats.jsp',
    'reportFormat': 'Y',
    'stat0': 'fichas.fechano',
    'variables': []
}

DEFINESTATS_POST_URL = 'https://www.desinventar.net/DesInventar/definestats.jsp'  # noqa
STATISTICS_POST_URL = 'https://www.desinventar.net/DesInventar/statistics.jsp'


def run():
    for i, country in enumerate(countries):
        try:
            code = country.lower()
            url = 'https://www.desinventar.net/DesInventar/profiletab.jsp?countrycode={}&continue=y'

            resp = requests.get(url.format(code))
            cookie = resp.headers['Set-Cookie'].split(';')[0]

            # POST DEFINESTATS
            #  set cookies
            HEADERS['Cookie'] = cookie
            HEADERS['Referer'] = HEADERS['Referer'].format(code)
            resp = requests.post(DEFINESTATS_POST_URL, headers=HEADERS, data=DEFINESTATS_BODY)

            soup = Soup(resp.text, 'html.parser')
            vars = []
            avail = []
            for select in soup.find_all('select'):
                if select.attrs['name'] == 'availableVars':
                    for option in select.find_all('option'):
                        avail.append(option.attrs['value'])
                elif select.attrs['name'] == 'variables':
                    for option in select.find_all('option'):
                        vars.append(option.attrs['value'])
            # now post for statistics
            body = dict(STATISTICS_POST_BODY)
            body['variables'] = avail
            headers = dict(HEADERS)
            headers['Cookie'] = cookie
            headers['Referer'] = 'https://www.desinventar.net/DesInventar/definestats.jsp'
            resp = requests.post(STATISTICS_POST_URL, headers=headers, data=body)
            # ignore this, we already have url for downloading spreadsheet

            csv_href = 'https://www.desinventar.net/DesInventar/stats_spreadsheet.jsp'
            headers = dict(HEADERS)
            headers['Cookie'] = cookie
            headers['Referer'] = 'https://www.desinventar.net/DesInventar/statistics.jsp'
            headers['Upgrade-Insecure-Requests'] = '1'
            resp = requests.get(csv_href, headers=headers)
            with open('{}.xls'.format(code), 'wb') as f:
                f.write(resp.content)
            print('{} DONE FOR {}'.format(i+1, country))
        except Exception as e:
            import traceback
            print(traceback.format_exc())


if __name__ == '__main__':
    run()

