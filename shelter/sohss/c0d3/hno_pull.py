"""read in HNO data, convert ISOz"""
from collections import OrderedDict
import re

import pandas as pd
import country_converter as coco


def get_cnt(cnts):
    """extract ISO from country field, replace unknown ISOs, make sure no duplicating bad names"""

    repl = {'2014 Revised Strategic Response Plan Sudan': 'Sudan',
            '2016 Humanitarian Response Plan': 'Iraq',
            '2017 Humanitarian Needs Overview Congo': 'Congo',
            'Emergency Humanitarian Response Plan REVISION 2008': 'Kenya',
            'Philippine: Typhoon Haiyan (Yolanda) Strategic Response Plan 2014': 'Philippines',
            'Strategic Response Plan 2014 Occupied Palestian Territory': 'Palestine',
            'Sudanese Red Crescent Society Emergency appeal 2014': 'Sudan'}

    cnts = [repl[v] if v in repl else v for v in cnts]

    assert (len([v for v in cnts if v in repl]) == len(set([v for v in cnts if v in repl])))
    assert ('not found' not in cnts)

    return coco.convert(names=cnts, to='ISO3')


def get_dims(dim):
    """get dims, as the output is currently jumbled.
        dims: up to a comma seperated triplet, same with subdim
    """
    types = ['Earthquake',
             'Floods',
             'Tropical Storm/Typhoon/Hurricane',
             'Conflict',
             'Other']

    presence = ['Activated',
                'Not Activated',
                'Informal Sectoral Working Group']

    decomp = OrderedDict({
        'dis_type': [],
        'year': [],
        'pres_type': [],
        'src_type': []
    })

    if type(dim) != float:
        vals = [v.strip() for v in reversed(dim.split(','))]

        for v in vals:
            if v in types:
                decomp['dis_type'].append(v)
            elif v in presence:
                decomp['pres_type'].append(v)
            elif re.match('(.*[0-9])', v):
                decomp['year'].append(re.match('(.*[0-9])', v).groups()[0])
            else:
                decomp['src_type'].append(v)

    for k, v in decomp.items():
        if len(v) == 0:
            decomp[k] = None
        elif len(v) == 1:
            decomp[k] = v[0]

    return [v for v in decomp.values()]


def get_ass_type(x):
    assert (str(x).count(',') <= 1)
    return x


def trim_cols(hno):
    return pd.DataFrame(hno[[
        'hno_date_of_lead_publication',
        'hno_imported_by',
        'hno_date_imported',
        'hno_lead_title',
        'hno_source',
        'hno_assignee',
        'hno_number_of_people_affected_shelter',
        'hno_number_of_people_affected_nfi',
        'hno_number_of_people_affected_total_(shelter_+_nfi)',
        'hno_number_of_people_affected_total_(all_sectors)',
        'hno_number_of_people_in_need_shelter',
        'hno_number_of_people_in_need_nfi',
        'hno_number_of_people_in_need_total_(shelter_+_nfi)',
        'hno_number_of_people_in_need_total_(all_sectors)',
        'hno_number_of_people_in_acute_need_shelter',
        'hno_number_of_people_in_acute_need_nfi',
        'hno_number_of_people_in_acute_need_total_(shelter_+_nfi)',
        'hno_number_of_people_in_acute_need_total_(all_sectors)',
        'hno_number_of_people_targeted_with_assistance_shelter',
        'hno_number_of_people_targeted_with_assistance_nfi',
        'hno_number_of_people_targeted_with_assistance_total_(shelter_+_nfi)',
        'hno_number_of_people_targeted_with_assistance_total_(all_sectors)',
        'hno_number_of_people_reached_with_assistance_shelter',
        'hno_number_of_people_reached_with_assistance_nfi',
        'hno_number_of_people_reached_with_assistance_total_(shelter_+_nfi)',
        'hno_number_of_people_reached_with_assistance_total_(all_sectors)',
        'hno_number_of_people_covered_with_assistance_shelter',
        'hno_number_of_people_covered_with_assistance_nfi',
        'hno_number_of_people_covered_with_assistance_total_(shelter_+_nfi)',
        'hno_number_of_people_covered_with_assistance_total_(all_sectors)',
        'hno_funds_requested_shelter',
        'hno_funds_requested_total',
        'hno_funds_recieved_shelter',
        'hno_funds_recieved_total',
        'hno_count_count',
        'hno_idps_count',
        'hno_refugees_count',
        'hno_count_international_ngo',
        'hno_count_national_ngo',
        'hno_count_national_government',
        'hno_count_total',
        'hno_iso3',
        'hno_disaster_type',
        'hno_year',
        'hno_presence_type',
        'hno_source_type',
        'hno_ass_type',
        'hno_uid']])


def pull():
    LOC = '../d0cz/hno_hrp_deep_export.xlsx'
    hno = pd.read_excel(LOC, sheet_name='Grouped Entries')
    hno.columns = ['hno_' + v.lower().strip().replace(' - ', '_')
        .replace(' ', '_').replace('-', '') for v in hno.columns.values]

    # get dims and colz
    hno['hno_iso3'] = get_cnt(hno.hno_lead_title)
    hno[['hno_disaster_type', 'hno_year', 'hno_presence_type', 'hno_source_type']] = \
        hno.apply(lambda x: pd.Series(get_dims(x['hno_subdimension'])), axis=1)
    hno['hno_ass_type'] = hno.apply(lambda x: get_ass_type(x['hno_subdimension.2']), axis=1)

    # drop vals without a year, as they're duplicates
    hno = hno[~hno['hno_year'].isnull()]

    hno['hno_uid'] = hno['hno_iso3'] + hno['hno_year']

    return trim_cols(hno)