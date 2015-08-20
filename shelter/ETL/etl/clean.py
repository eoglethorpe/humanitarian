import etl

def algo1(db, ref):
    #***Column A must be in Reference>ImplementingAgency if not: make a note
    db_col_loc = etl.find_in_header(db, 'Implementing agency')
    ref_col_loc = etl.find_in_header(ref,'Implementing_Agency_Name')
    missing_names = etl.colvals_notincol(db, db_col_loc, ref, ref_col_loc)
    return 'The following agencies are not in the reference:\n' + ','.join(missing_names)

def algo2(db,ref):
    #Column B: If == Implementing Agency set Column B=Internal
    #assumes they are next to each other
    db_col_loc_impl = etl.find_in_header(db, 'Implementing agency')
    db_col_loc_source = etl.find_in_header(db, 'Sourcing Agency')
    vals_changed = []

    for row in db.iter_rows(db_col_loc_impl + "2:" + 
        etl.find_last_value(db, db_col_loc_source, 'c')):
            if row[0].value == row[1].value:
                vals_changed.append(str(row[1].row))
                row[1].value = 'INTERNAL'

    return 'The following rows were marked as internal:\n' + ','.join(vals_changed)

def algo(db,ref):
    print 'x'