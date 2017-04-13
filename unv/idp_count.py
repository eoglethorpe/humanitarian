import csv
import os

import requests
from xlsxwriter.workbook import Workbook
from bs4 import BeautifulSoup



#district_cd goes up to 75
#zone_cd goes up to 15
#st_cd goes up to 5
BASE_URL = 'http://116.90.236.110/cms/victims/reports/ExternalReport/displaced.php?mode=export&per_district_cd=' \
           '&per_reg_st_cd=&per_zone_cd=&search_cd=1&full_name_loc_like=&conflict_type_cd=8&bef_district_cd=%s&' \
           'bef_reg_st_cd=%s&bef_zone_cd=%s&aft_district_cd='

def export_to_xlsx(data, filename, reverse=False):
    """ export_to_xlsx(data, chart, filename): Exports data to an Excel Spreadsheet.
    Data should be a dictionary with rows as keys; the values of which should be a dictionary with columns as keys; the value should be the value at the x, y coordinate.
    Chart should be either True, in which case the values will be generated, or a dictionary with the following keys:
        type: string, choose from: line, ...
        series: list of dictionaries with the following: name, categories, values
        title, xaxis_title, yaxis_title: strings
        style: int
        cell
        x_offset
        y_offset
    Reverse is used to signal whether to reverse the row order or not (except for the header/first row)
    """

    workbook = Workbook(filename)
    worksheet = workbook.add_worksheet()

    for (row, x) in enumerate([sorted(data.keys())[0]] + list(
            reversed(sorted(data.keys())))) if reverse is True else enumerate(sorted(data.keys())):
        for y in sorted(data[x].keys()):
            try:
                worksheet.write(x, y, data[x][y])
            except ValueError:
                worksheet.write(x, y, '' if data[x][y] == '---' else data[x][y])

    workbook.close()

    return


def html_table_to_excel(table):

    """ html_table_to_excel(table): Takes an HTML table of data and formats it so that it can be inserted into an Excel Spreadsheet.
    """

    data = {}
    tbl = open(table, 'r')
    soup = BeautifulSoup(tbl, 'html.parser')

    for(x, row) in enumerate(soup.findAll("tbody")[0].findAll('tr')):
        columns = row.findAll('td')
        data[x] = {}
        for (y, col) in enumerate(columns):
            data[x][y] = col.text

    return data

def get_nums():
    """get district nums"""
    nums = []

    with open(os.getcwd() + '/idp_dl/nums.csv', 'r') as f:
        reader = csv.reader(f)
        for row in reader:
            nums.append(row)

    return nums

def guicci_main():
    nums = get_nums()
    for n in nums:
        print('fetching ' +  BASE_URL % (n[2], n[0], n[1]))
        r = requests.get(BASE_URL % (n[2], n[0], n[1]))
        export_to_xlsx(html_table_to_excel(r.text), (os.getcwd() + '/idp_dl/%s-%s-%s.csv' % (n[2], n[0], n[1])))
        print('fetched!')

if __name__ == '__main__':
    # tbl = open('/Users/ewanog/code/repos/humanitarian/unv/displaced.xls', 'r')
    # export_to_xlsx(html_table_to_excel(tbl.read()))

    guicci_main()