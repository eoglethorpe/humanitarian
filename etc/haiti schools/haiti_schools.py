"""take in an xlsx file of schools lat long and extract admin level """
#http://stackoverflow.com/questions/7861196/check-if-a-geopoint-with-latitude-and-longitude-is-within-a-shapefile

from zipfile import ZipFile
import csv

import fiona
from shapely.geometry import Point, asShape
from openpyxl import load_workbook
from django.utils.encoding import smart_str

def find():

    out = open('./out.csv', 'w')
    outwrite = csv.writer(out, delimiter=',')

    shapefile = fiona.open("/Users/ewanog/code/repos/humanitarian/etc/haiti schools/ht3/hti_admnbnda_adm3_CNIGS2013.shp")
    w = load_workbook("/Users/ewanog/code/repos/humanitarian/etc/haiti schools/list.xlsx")
    for row in w.get_sheet_by_name('ocha').rows[1:]:
        long = row[0].value
        lat = row[1].value
        name = row[2].value
        found = False

        cyc = shapefile

        for k,v in shapefile.items():
            # In this case, we'll assume the shapefile only has one record/layer (e.g., the shapefile
            # is just for the borders of a single country, etc.).


            # Use Shapely to create the polygon
            shape = asShape(v['geometry'])
            point = Point(long, lat) # longitude, latitude

            # Alternative: if point.within(shape)
            if shape.contains(point):
                print name
                outwrite.writerow([smart_str(name),long,lat,
                                    v['properties']['admin1pcod'], v['properties']['admin2pcod'], v['properties']['admin3pcod'],
                                   v['properties']['admin1name'], v['properties']['admin2name'], v['properties']['admin3name']])
                found = True
                break

    if not found:
        print('not found for ' + name)
        outwrite.writerow([smart_str(name), 'not found'])

if __name__=='__main__':
    find()