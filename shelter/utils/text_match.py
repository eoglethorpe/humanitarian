"""A module to iterate through a list of known and possibly mispelled
    words in order to easily find correct spellings
"""

#TODO: create GUI or CLI commands
##store corrected words
##option to skip
##parameterize limit nubmer of matches
##not show VDCs as possilb emathces taht are already added
##store progress as progressing incase it fucks up


from fuzzywuzzy import fuzz
from fuzzywuzzy import process
import csv
import os

MATCH_LIMIT = 6
DIR_LOCATION = '/Users/ewanog/code/nepal-earthquake/shelter/utils/'

def import_text():
    """read in two columns for known text and text to match"""
    known = []
    match = []


    f = open('%stext.csv'%DIR_LOCATION, 'rU')
    reader = csv.DictReader(f)

    #read in csv, assumes there is a col = known and one = match
    for row in reader:
        if row['known'] != '':
            known.append(row['known'])
        
        if row['match'] != '':
            match.append(row['match'])

    return known, match


def check_matches(known, match):
    """iterate over known words looking for matches""" 
    #array containing tuples of corrected spellings
    out_vals = []

    #clear screen
    os.system('clear')
    
    for val in known:
        cur_matches = process.extract(val, match, limit = MATCH_LIMIT)
        
        #append a none option and option for actual val
        cur_matches.append(("NONE",0))
        cur_matches.append((val,100))


        #if there is a match of 100, skip
        if cur_matches[0][1] != 100:
            #print out options for each word
            print_options(val, cur_matches)

            #cycle through prompt for input if valid (numeric, within MATCH_LIMIT)
            choice = None
            while choice == None:
                try:
                    choice = cur_matches[get_choice()][0]
                except:
                    print '!Invalid match! Try again'
                    print_options(val, cur_matches)
    
            print choice

        else:
            choice = val
            print '%s - Match!'%choice

        print 
        print
        #create a new tuple with correct and incorrect spelling
        out_vals.append((val, choice))

    #we're done, return vals array
    return out_vals

def get_choice():
    """prompt to get valid int choice between 0 and MATCH_LIMIT"""
    response = raw_input().rstrip("\n")

    if not response.isdigit():
        get_choice()

    if not 0 <= int(response) < MATCH_LIMIT+2:
        get_choice()

    return int(response)


def print_options(val, cur_matches):
    """print options for a text match"""
    print val
    for i in xrange(MATCH_LIMIT+2):
        print "[%i] %s : %s "%(i, cur_matches[i][0], cur_matches[i][1])

    print 
    print 'Choice?'
        

def output(out_vals):
    f = open('%scorrected.csv'%DIR_LOCATION, 'wt')
    writer = csv.writer(f)
    writer.writerow(['original','corrected'])
    for row in out_vals:
        writer.writerow([row[0],row[1]])


if __name__ =='__main__':
    known, match = import_text()
    out_vals = check_matches(known, match)
    output(out_vals)