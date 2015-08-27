"""Module for extracting data from dropbox and aggregating"""
#TODO: better way for specifyign which folder to pull from (latest?)
##how to handle names?
##pull from rules based text file
##log put on dbox, make better
##test individual cleaning
##mvoe current logs to an 'old' file 
##put in run params: test, exclude, folder location?
##change to pull down all WSs at same time as opposed to iterating  


import dropbox
import clean
import os
import cStringIO
import re
from openpyxl import load_workbook
from openpyxl.cell import column_index_from_string
from openpyxl import Workbook
import openpyxl.writer.excel as wrtex
import time

#dropbox setup
db_access = os.environ['db_access']
client = dropbox.client.DropboxClient(db_access)

DB_PATH = '/2015 Nepal EQ/04 IM/Reporting/Database_&_Template/Data_Cleaning_and_Validation/'
TEST_FILE = '/test_sheet.xlsx'

def iterate_reports():
    """cycle through all reports contained in dbox directory"""

    meta = client.metadata(DB_PATH, list=True)
    file_list = [str(f['path']) for f in meta['contents'] if re.search('xls|xlsx$',str(f))]
    
    k = []
    for v in file_list:
        if 'C-' in v or 'C -' in v:
            k.append([v])
            print 'pulled: ' + v

    file_list = k[0]

    print 'list is!: ' 
    for v in file_list:
        print v

#    for v in exclude:
#        file_list.remove(v)

#    file_list = [DB_PATH+"/Welthungerhilfe.xlsx/"]

    action = 'consolidate'
    wbs = []

    for f in file_list:
        #pull down workbook from specified directory
        print "pulling! " + f
        wb_current = pull_wb(f)

        #check to see if properly formatted
        if wb_format(wb_current):
            if action == 'consolidate':
                print 'appended ' + f
                wbs.append(wb_current)

            else:
                #clean the workboook
                print "cleaning " + f
                clean_file(wb_current, f)

        else:
            #put in malformatted folder
            print 'malformatted ' + f
            path = DB_PATH + '/old_format_or_incorrect/' + f.rsplit('/', 1)[1]
            #send_wb(path, wb_current)

    print 'consolidating...'
    to_send = consolidate(pull_wb('/2015 nepal eq/04 im/reporting/Database_&'
        +'_Template/EO_testing/baseline_trim.xlsx').get_sheet_by_name('Database'), wbs, 'V')
    send_wb('/2015 nepal eq/04 im/reporting/Database_&_Template/EO_testing/' +
        'merged.xlsx', to_send)


def consolidate(baseline, wbs, key_col):
    """consolidate baseline data and worksheets into one sheet 
        and remove duplicates"""

    print 'in consolidate'

    cons_wb = Workbook()
    cons = cons_wb.active
    cons.title = 'Consolidated'
    cons.append(get_values(baseline.rows[0]) + ['UID'])

    print 'step1'

    merge_sheets = []
    #pull out desired worksheet
    for wb in wbs:
        print 'step2'
        merge_sheets.append(wb.get_sheet_by_name('Distributions'))

    print 'step3'

    #read in baseline db and new WSs into dictionaries
    base_dict = {}
    merge_sheets_dict = {}
    key_loc = column_index_from_string(key_col)-1

    print 'step4'


    #add in UID value for sheets
    #there is a problem where imaginary columns are being retruned by .rows, so we find the
    #max value of the header and only look for values of that row that extend out to that column
    for wb in merge_sheets:
        test_c = 0
        print 'step5'
        max_val = len(wb.rows[0])
        for r in wb.rows[1:]:
            test_c+=1
            if test_c % 100 == 0:
                print test_c
            wb[key_col + xstr(r[0].row)] = get_uid(r[0:max_val], wb)


    print 'in 1'

    #add UID for baseline
    max_val = len(baseline.rows[0])
    for r in baseline.rows[1:]:
        baseline[key_col + xstr(r[0].row)] = get_uid(r[0:max_val], baseline)
    print 'in 2'

    #add baseline to dict
    for r in baseline.rows[1:]:
        base_dict[xstr(r[key_loc].value)] = get_values(r)
    print 'in 3'

    #merge sheets into a dict
    for wb in merge_sheets:
        for r in wb.rows[1:]:
            merge_sheets_dict[xstr(r[key_loc].value)] = get_values(r)
    print 'in 4'

    dup_count = 0
    #go through baseline and remove dups
    for k in base_dict.keys():
        if k in merge_sheets_dict.keys():
            base_dict.pop(k)
            dup_count+=1

    print 'in 5'
    print 'dupcount: ' + str(dup_count)

    #now, add baseline and then wbs to cons
    for v in base_dict.values():
        cons.append(v)
    print 'in 6'

    for v in merge_sheets_dict.values():
        cons.append(v)
    
    return cons_wb

def get_uid(row, sheet):
    vals = ["Implementing agency", "Local partner agency" , "District", 
            "VDC / Municipalities", "Municipal Ward", "Action type", 
            "Action description", "# Items / # Man-hours / NPR",
            "Total Number Households"]
    key = ""

    for v in vals:
        key += xstr(row[column_index_from_string(find_in_header(sheet, v))-1].value)

    return key

def get_values(r):
    """returns values of a row or a column"""
    ret = []
    for v in r:
        ret.append(xstr(v.value))

    return ret

def send_wb(path, wb):
    print 'sending! ' + path
    client.put_file(path, wrtex.save_virtual_workbook(wb))


def wb_format(wb):
    """check to see if a report is correct and in the new report format"""
    must_contain = ['Distributions', 'Training', 'Reference']

    match_count = 0
    for s in wb.worksheets:
        if s.title in must_contain:
            match_count+=1

    if match_count < 3:
        return False
    else:
        return True

def clean_file(wb, path): 
    """cycle through a report and apply cleaning algorithms"""
    
    #get our two sheets
    db = wb.get_sheet_by_name('Distributions')
    ref = wb.get_sheet_by_name('Reference')

    #setup log
    rname =  path.rsplit('/', 1)[1]
    report_line = '******Report for ' + rname + ' ******'
    report_a_log(report_line, rname)


    #####do edit stuff
    #algos return db, ref, message

    #algo1
    db, ref, message = clean.algo1(db,ref) 
    report_a_log(message, rname)

    #algo2
    db, ref, message = clean.algo2(db,ref)
    report_a_log(message, rname)

    #algo3
#    db, ref, message = clean.algo3(db,ref)
#    report_a_log(message, rname)

    #algo4
    db, ref, message = clean.algo4(db,ref)
    report_a_log(message, rname)

    #algo5
    db, ref, message = clean.algo5(db,ref)
    report_a_log(message, rname)

    #algo6
    db, ref, message = clean.algo6(db,ref)
    report_a_log(message, rname)

    #algo7
    db, ref, message = clean.algo7(db,ref)
    report_a_log(message, rname)

    #algo8
    db, ref, message = clean.algo8(db,ref)
    report_a_log(message, rname)

    #algo9
    db, ref, message = clean.algo9(db,ref)
    report_a_log(message, rname)

    #algo10
    db, ref, message = clean.algo10(db,ref)
    report_a_log(message, rname)

    #algo11
    db, ref, message = clean.algo11(db,ref)
    report_a_log(message, rname)

    #algo12
    db, ref, message = clean.algo12(db,ref)
    report_a_log(message, rname)

    #algo13
    db, ref, message = clean.algo13(db,ref)
    report_a_log(message, rname)

    #algo14
    db, ref, message = clean.algo14(db,ref)
    report_a_log(message, rname)

    #algo15
    db, ref, message = clean.algo15(db,ref)
    report_a_log(message, rname)

    #algo16
    db, ref, message = clean.algo16(db,ref)
    report_a_log(message, rname)

    #algo17
    db, ref, message = clean.algo17(db,ref)
    report_a_log(message, rname)

    #algo18
    db, ref, message = clean.algo18(db,ref)
    report_a_log(message, rname)

    #algo19
    db, ref, message = clean.algo19(db,ref)
    report_a_log(message, rname)


    #dummy empty log to send to finalize logging
    report_a_log(' ','text')

    #upload with name of file at end
    #we need to upload the new version!!!!!!!!
    send_wb(DB_PATH + '/edited/' + path.rsplit('/', 1)[1], wb)
    print 'uploaded! ' + path

report_recvd = False
current_path = ''
current_log = []

def report_a_log(log_value, path):
    """write out contents for a given log - creates new entry if a new path is given"""
    #todo: this is gross
    global report_recvd
    global current_path
    global current_log


    #if module is starting and we haven't logged anything
    if not report_recvd:
        current_path = path
        report_recvd = True
    

    #if we are recieving a new path
    elif current_path != path:
        current_path = path
        
        #write out
        with open('/Users/ewanog/code/nepal-earthquake/shelter/etl/etl/logs/cleaned_log'+
            time.strftime("%m-%d-%y_%H:%M_%S") +'.txt', 'w') as f:
            for log in current_log:
                f.write(str(log)+'\n')
        f.close()

        #move on to next log
        current_log.append('')
        current_log.append('')

    current_log.append(log_value)
    current_log.append('')



def find_in_header(sheet, find_val):
    """find the coordinate of a value in header (assumes header is in row 1)"""
    for row in sheet.iter_rows('A1:' + find_last_value(sheet,'A','r')):
        for cell in row:
            if cell.value == find_val:
                return cell.column

    #if we haven't returned anything yet
    print 'No header found for: ' + find_val
    return None

def colvals_notincol(sheet_val,col_val,sheet_ref,col_ref):
    """return values from a column that are NOT in a reference column"""
    not_in = []
    to_search = []

    #create an array from sheet_ref with values to be searched (as opposed to nested loops)
    #iter_rows syntax: sheet.iter_rows('A1:A2')
    for row in sheet_ref.iter_rows(col_ref + "2:" + 
        find_last_value(sheet_ref, col_ref, 'c')):

        for cell in row:               
                try:
                    to_search.append(xstr(cell.value))
                except:
                    to_search.append(str(cell.value))

    #now search through vals and see if they're present
    for row in sheet_val.iter_rows(col_val + "2:" + 
        find_last_value(sheet_val, col_val, 'c')):

        for cell in row:
            if str(cell.value) not in to_search:
                try:
                    not_in.append(xstr(cell.value))
                except:
                    not_in.append(str(cell.value))

    return not_in
             


def find_last_value(sheet, start_location, r_or_c):
    """find position of last value in a given row or column"""
    #extract form r_or_c if we should be iterating a row or column
    
    row_it = 0
    col_it = 0
    if r_or_c == 'c':
        row_it = 1
    elif r_or_c == 'r':
        col_it = 1
    else:
        raise Exception("r_or_c must be r or c!")
    
    #look for a cell without value, and if we find a blank, traverse 100 more
    #to make sure there's no blanks
    blank_count = 0
    found = False
    cur_cell = sheet[start_location+'1']
    while not found:
        cur_cell = cur_cell.offset(row = row_it, column = col_it)

        if not cur_cell.value:
            if blank_count == 0:
                #coord of a cell step back 1
                last_found = cur_cell.offset(row = -row_it, column= -col_it).coordinate
                blank_count+=1

            elif blank_count == 100:
                found = True
            else:
                blank_count+=1
        else:
            blank_count=0

    return last_found


def pull_wb(location):
    """return an excel pulled from dropbox"""

    in_mem_file = pull_file(location)

    wb = load_workbook(in_mem_file, data_only = True)
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

def xstr(conv):
    """return a properly encoded string"""
    try:
        return conv.encode('utf8')
    except:
        return str(conv)

def test():
    return load_workbook('/Users/ewanog/code/nepal-earthquake/shelter/etl/clean_test.xlsx', data_only=True)

if __name__ == '__main__':
    iterate_reports()

