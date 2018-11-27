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
import sys
import collections

MATCH_LIMIT = 6
DIR_LOCATION = 'text.csv'

def import_text():
    """read in two columns for known text and text to match"""
    known = collections.OrderedDict()
    match = collections.OrderedDict()

    f = open(DIR_LOCATION, 'rU')
    reader = csv.DictReader(f)

    #read in csv, assumes there is a col = known and one = match
    for row in reader:
        if row['known'] != '':
            known[row['known']] = row['known_prop']

        if row['match'] != '':
            match[row['match']] = row['match_prop']

    return known, match


def check_matches(known, match):
    """iterate over known words looking for matches""" 
    #array containing tuples of corrected spellings
    out_vals = []

    #clear screen
    os.system('clear')
    
    for k,v in known.iteritems():
        matched_vals = [ik for ik, iv in match.iteritems() if iv == v]
        cur_matches = process.extract(k, matched_vals, limit = MATCH_LIMIT)
        
        #append a none option and option for actual val
        cur_matches.insert(0,("NONE",0))
        cur_matches.append((k,100))


        #if there is a match of 100, skip
        if cur_matches[1][1] == 86 or cur_matches[1][1] < 50:
            #special case where probably means there really isn't a match
            choice = 'NONE'
            print 'No match!'

        elif cur_matches[1][1] < 95:
            #print out options for each word
            print_options(k, cur_matches)

            #cycle through prompt for input if valid (numeric, within MATCH_LIMIT)
            choice = None
            while choice == None:
                try:
                    choice = cur_matches[get_choice()][0]
                except:
                    print '!Invalid match! Try again'
                    print_options(k, cur_matches)
    
            print choice

        else:
            #exact match
            choice = cur_matches[1][0]
            print '%s - Match!'%choice

        print 
        print
        #create a new tuple with correct and incorrect spelling
        out_vals.append((k, choice))
        output(out_vals)

    #we're done, return vals array
    return out_vals

def get_choice():
    """prompt to get valid int choice between 0 and MATCH_LIMIT"""
    response = raw_input().rstrip("\n")

    if response == 'exit':
        #this doesn't work
        raise SystemExit()

    if not response.isdigit():
        get_choice()

    if not 0 <= int(response) < MATCH_LIMIT+2:
        get_choice()

    return int(response)


def print_options(val, cur_matches):
    """print options for a text match"""
    print val

    #skip one to print none at end
    for i,v in enumerate(cur_matches[1:]):
        print "[%i] %s : %s "%(i+1, v[0], v[1])
    print "[%i] %s : %s " % (0, cur_matches[0][0], cur_matches[0][1])

    print 
    print 'Choice?'
        

def output(out_vals):
    f = open('corrected.csv', 'wt')
    writer = csv.writer(f)
    writer.writerow(['original','corrected'])
    for row in out_vals:
        writer.writerow([row[0],row[1]])


if __name__ =='__main__':
    known, match = import_text()
    out_vals = check_matches(known, match)
    output(out_vals)