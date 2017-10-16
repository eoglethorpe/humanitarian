"""iteratate through all the existing csv sheets, make apprioriate HTML files, take screenerz"""
from os import listdir, system
from os.path import isfile, join
import re

from selenium.webdriver import Safari

browser = Safari()
PATH = './data/xls/out/'

def take_screen(html_add):
    p = re.compile(r'(\d{6})')
    match = re.findall(p, html_add)
    LOCAL_HOST = 'http://127.0.0.1:8080/html/'
    browser.get('http://127.0.0.1:8080/' + html_add)
    browser.get_screenshot_as_file('./screen/{0}'.format(match[0]) + '.png')

def make_html(doc):
    # Read in the file
    # with open('{0}{1}'.format(PATH, doc), 'r') as file:
    with open('base.html', 'r') as file:
        filedata = file.read()

    # Replace the target string
    filedata = filedata.replace('CSVFILENAMETOCHANGE', '../' + PATH + doc.split('.')[0])

    # Write the file out again
    html_file = './html/{0}.html'.format(doc.split('.')[0])
    with open(html_file , 'w') as file:
        file.write(filedata)

    return html_file


def main():
    #make sure to run http-server for npm server to be up
    try:
        for doc in [f for f in listdir(PATH) if isfile(join(PATH, f)) and f[0] not in ['.', '~']]:
            file = make_html(doc)
            take_screen(file)
    finally:
        browser.quit()

if __name__ == '__main__':
    main()