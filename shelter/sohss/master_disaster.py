
def main():
    pass

def fetch_api():
    data = []
    for i in range(4):
        with urllib.request.urlopen("https://api.reliefweb.int/v1/disasters?appname=vocabulary"
                                    "&preset=external&limit=1000&offset={}".format(i*1000)) as url:
            data += json.loads(url.read().decode())['data']

    return data

def check_dates():
    """check to see if all names have date in them

        names are either in format of:
            MMM YYYY
            OR
            YYYY-YYYY

        if not in first format, check to see if end year > 2005
    """
    MIN_YEAR = 2015
    data = fetch_api()

    for v in data:
        name = v['fields']['name'][-8:]
        if not name[0:3].isalpha():
            print(name)



if __name__ == '__main__':
    check_dates()
    # main()