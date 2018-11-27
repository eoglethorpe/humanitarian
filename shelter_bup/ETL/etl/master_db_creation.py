"""read in master db file and upload it to SQL"""
#TODO: read in DDL from xls or somethign better

from sqlalchemy import create_engine

import os
import sys
from sqlalchemy import Column, Integer, String, Float
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
import click
import dropbox
import etl
from openpyxl.cell import column_index_from_string


#SQLA
Base = declarative_base()
engine = create_engine('postgresql://shelter:clusterdata@sheltercluster.ci0kkoh87sga.us-east-1.rds.amazonaws.com:5432/shelter')
Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)
session = DBSession()

#dbox
db_access = os.environ['db_access']
client = dropbox.client.DropboxClient(db_access)

def Distributions(Base):
    """create table"""

    """
    Priority : priority
    Hard to Reach Access Methods : access_method
    Shelter Cluster Hub : hub
    Last Update	: as_of
    District HLCIT  Code : dist_code
    VDC / Municipality HLCIT  Code : vdc_code
    UNOCHA Activity Categories : act_cat
    Implementing agency	:	imp_agency
    Sourcing Agency	:	source_agency
    Local partner agency	:	local_partner
    Contact Name	:	contact_name
    Contact Email	:	contact_email
    Contact Phone Number	:	contact_phone
    District	:	district
    VDC / Municipalities	:	vdc
    Municipal Ward	:	ward
    Action type	:	act_type
    Action description	:	act_desc
    Targeting	:	targeting
    # Items / # Man-hours / NPR	:	quantity
    Total Number Households	:	total_hh
    Average cost per households (NPR)	:	avg_hh_cost
    Female headed households	:	fem_hh
    Vulnerable Caste / Ethnicity households 	:	vuln_hh
    Activity Status	:	act_status
    "Start date (Actual or Planned)"	:	start_dt
    "Completion Date (Actual or Planned)"	:	comp_dt
    Additional Comments	:	comments
    """

    __tablename__ = 'distributions'

    priority = Column(String(250))
    access_method = Column(String(250))
    hub = Column(String(250))
    as_of = Column(String(250))
    dist_code = Column(String(250))
    vdc_code = Column(String(250))
    act_cat = Column(String(250))
    imp_agency = Column(String(250))
    source_agency = Column(String(250))
    local_partner = Column(String(250))
    contact_name = Column(String(250))
    contact_email = Column(String(250))
    contact_phone = Column(String(250))
    district = Column(String(250))
    vdc = Column(String(250))
    ward = Column(String(250))
    act_type = Column(String(250))
    act_desc = Column(String(250))
    targeting = Column(String(250))
    quantity = Column(Integer)
    total_hh = Column(Integer)
    avg_hh_cost = Column(Float)
    fem_hh = Column(Integer)
    vuln_hh = Column(Integer)
    act_status = Column(String(250))
    start_dt = Column(String(250))
    comp_dt = Column(String(250))
    comments = Column(String(250))
    pk = Column(String(250), primary_key=True)

@click.command()
@click.option('--path', help = 'path to spreadsheet')
def insert_data(path):
    """iterate over each row and add to db"""
    path = "/Users/ewanog/tmp/simp.xlsx"
    ws = etl.pull_wb(path, 'local').get_sheet_by_name('Distributions')
    locs = get_locs(ws)
    conn = engine.connect()
    ins = Base.metadata.tables['distributions'].insert()

    c=0
    for r in ws.rows[1:]:
        conn.execute(
        ins,
        priority=r[locs["priority"]-1].value,
        access_method=r[locs["access_method"]-1].value,
        hub=r[locs["hub"]-1].value,
        as_of=r[locs["as_of"]-1].value,
        dist_code=r[locs["dist_code"]-1].value,
        vdc_code=r[locs["vdc_code"]-1].value,
        act_cat=r[locs["act_cat"]-1].value,
        imp_agency=r[locs["imp_agency"]-1].value,
        source_agency=r[locs["source_agency"]-1].value,
        local_partner=r[locs["local_partner"]-1].value,
        contact_name=r[locs["contact_name"]-1].value,
        contact_email=r[locs["contact_email"]-1].value,
        contact_phone=r[locs["contact_phone"]-1].value,
        district=r[locs["district"]-1].value,
        vdc=r[locs["vdc"]-1].value,
        ward=r[locs["ward"]-1].value,
        act_type=r[locs["act_type"]-1].value,
        act_desc=r[locs["act_desc"]-1].value,
        targeting=r[locs["targeting"]-1].value,
        quantity=r[locs["quantity"]-1].value,
        total_hh=r[locs["total_hh"]-1].value,
        avg_hh_cost=r[locs["avg_hh_cost"]-1].value,
        fem_hh=r[locs["fem_hh"]-1].value,
        vuln_hh=r[locs["vuln_hh"]-1].value,
        act_status=r[locs["act_status"]-1].value,
        start_dt=r[locs["start_dt"]-1].value,
        comp_dt=r[locs["comp_dt"]-1].value,
        comments=r[locs["comments"]-1].value,
        pk=gen_pk(r, locs))

def gen_pk(r, locs):
    return etl.xstr(r[locs["imp_agency"]-1].value)+etl.xstr(r[locs["local_partner"]-1].value)+etl.xstr(r[locs["district"]-1].value)+etl.xstr(r[locs["vdc"]-1].value)+etl.xstr(r[locs["ward"]-1].value)+etl.xstr(r[locs["act_type"]-1].value)+etl.xstr(r[locs["act_desc"]-1].value)+etl.xstr(r[locs["quantity"]-1].value)+etl.xstr(r[locs["total_hh"]-1].value)


def get_locs(ws):
    """find column headers in advance so we don't have to call each time"""
    ret = {}
    ret["priority"]=column_index_from_string(etl.find_in_header(ws,"Priority"))
    ret["access_method"]=column_index_from_string(etl.find_in_header(ws,"Hard to Reach Access Methods"))
    ret["hub"]=column_index_from_string(etl.find_in_header(ws,"Shelter Cluster Hub"))
    ret["as_of"]=column_index_from_string(etl.find_in_header(ws,"Last Update"))
    ret["dist_code"]=column_index_from_string(etl.find_in_header(ws,"District HLCIT Code"))
    ret["vdc_code"]=column_index_from_string(etl.find_in_header(ws,"VDC / Municipality HLCIT Code"))
    ret["act_cat"]=column_index_from_string(etl.find_in_header(ws,"UNOCHA Activity Categories"))
    ret["imp_agency"]=column_index_from_string(etl.find_in_header(ws,"Implementing agency"))
    ret["source_agency"]=column_index_from_string(etl.find_in_header(ws,"Sourcing Agency"))
    ret["local_partner"]=column_index_from_string(etl.find_in_header(ws,"Local partner agency"))
    ret["contact_name"]=column_index_from_string(etl.find_in_header(ws,"Local Contact Name"))
    ret["contact_email"]=column_index_from_string(etl.find_in_header(ws,"Local Contact Email"))
    ret["contact_phone"]=column_index_from_string(etl.find_in_header(ws,"Local Contact Phone #"))
    ret["district"]=column_index_from_string(etl.find_in_header(ws,"District"))
    ret["vdc"]=column_index_from_string(etl.find_in_header(ws,"VDC / Municipalities"))
    ret["ward"]=column_index_from_string(etl.find_in_header(ws,"Municipal Ward"))
    ret["act_type"]=column_index_from_string(etl.find_in_header(ws,"Action type"))
    ret["act_desc"]=column_index_from_string(etl.find_in_header(ws,"Action description"))
    ret["targeting"]=column_index_from_string(etl.find_in_header(ws,"Targeting"))
    ret["quantity"]=column_index_from_string(etl.find_in_header(ws,"# Items / # Man-hours / NPR"))
    ret["total_hh"]=column_index_from_string(etl.find_in_header(ws,"Total Number Households"))
    ret["avg_hh_cost"]=column_index_from_string(etl.find_in_header(ws,"Average cost per households (NPR)"))
    ret["fem_hh"]=column_index_from_string(etl.find_in_header(ws,"Female headed households"))
    ret["vuln_hh"]=column_index_from_string(etl.find_in_header(ws,"Vulnerable Caste / Ethnicity households"))
    ret["act_status"]=column_index_from_string(etl.find_in_header(ws,"Activity Status"))
    ret["start_dt"]=column_index_from_string(etl.find_in_header(ws,"Start date"))
    ret["comp_dt"]=column_index_from_string(etl.find_in_header(ws,"Completion Date"))
    ret["comments"]=column_index_from_string(etl.find_in_header(ws,"Additional Comments"))
    return ret

if __name__ == '__main__':
    Base.metadata.tables['distributions'].drop(engine, checkfirst=True)
    Base.metadata.create_all(engine)
    insert_data()
    print 'done'