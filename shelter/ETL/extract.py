"""Module for extracting data from dropbox and aggregating"""
#TODO: better way for specifyign which folder to pull from (latest?)
##how to handle names?
##qualify sheets as being valid before cycling or skip invalid ones?


import dropbox
import os
import cStringIO
import re
from openpyxl import load_workbook


#dropbox setup
db_key = os.environ['db_key']
db_secret = os.environ['db_secret']
db_access = os.environ['db_access']
client = dropbox.client.DropboxClient(db_access)

DB_PATH = '/2015 Nepal EQ/04 im/reporting/Database_&_Template/Incoming/31 July 2015'
    
def iterate_reports():
    """cycle through all reports contained in dbox directory"""

    meta = client.metadata(DB_PATH, list=True)
    file_list = [str(f['path']) for f in meta['contents'] if re.search('xls|xlsx$',str(f))]
    file_list = ['/2015 nepal eq/04 im/reporting/database_&_template/Incoming/31 July 2015/ACTED - 30072015 - 4W Shelter.xlsx']
    for f in file_list:
        #pull down workbook from specified directory
        print "pulling " + f
        wb_current = pull_wb(f)

        #clean the workboook
        print "cleaning " + f
        clean_file(wb_current, f)


def clean_file(wb, path):
    """cycle through reports and apply cleaning algorithms"""
    database = wb.get_sheet_by_name('Database')
    ref = wb.get_sheet_by_name('Reference')

    #####do edit stuff

    #Column A must be in Reference>ImplementingAgency 
    ##if not: Add it to reference sheet



    #

    #upload with name of file at end
    client.put_file(DB_PATH + '/edited/' + path.rsplit('/', 1)[1], pull_file(path))
    print 'uploaded! ' + path


def find_last_entry(sheet, column):
    """find position of lowest row value in a given sheet"""
    found = False
    loc = 1
    while !found:
        if sheet[column+str(loc)].value:
            loc+=1
        else:
            found = True


def pull_wb(location):
    """return an excel pulled from dropbox"""

    in_mem_file = pull_file(location)

    wb = load_workbook(in_mem_file)
    print "pulled! " + str(wb.get_sheet_names())  
    in_mem_file.close()

    return wb

def pull_file(location):
    """pull a file from dropbox"""
    to_ret = cStringIO.StringIO()

    with client.get_file(location) as f:
        to_ret.write(f.read())
    f.close()

    return to_ret

if __name__ == '__main__':
    iterate_reports()
