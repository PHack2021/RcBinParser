'''
Main driver code
'''
import csv
import json
from pprint import pprint
from typing import List

from colorama import Fore
from sqlalchemy.orm import Session

from models import db_connect, create_table
from models import District, County_City, Organization, RcBin
from rc_bin_parser import CsvParser, PdfParser

from rc_bin_parser.utils import get_dict_from_csv

SOURCES_PATH = 'resources/sources.json'
skip_list = ['嘉義市']


def read_sources() -> List[dict]:
    with open(SOURCES_PATH, 'r', encoding='UTF-8') as f:
        sources = json.load(f)
    return sources


def push_to_db(**kwargs):
    # Connect to db and create tables
    engine = db_connect()
    session = Session(bind=engine)
    create_table(engine)

    # Update county_city
    county_cities = get_dict_from_csv('resources/county_city.csv')
    for county_city in county_cities:
        c = County_City()
        c.code = county_city['code']
        c.name = county_city['name']
        c.order = int(county_city['order'])

        if county_city.get('alt_name', ''):
            c.alt_name = county_city['alt_name']

        print(c.name)
        session.merge(c)
    session.commit()

    # Update district
    districts = get_dict_from_csv('resources/districts.csv')
    for district in districts:
        d = District()
        d.code = district['code']
        d.name = district['name']

        c = session.query(County_City).filter(
            County_City.code == district['code'][:5]).one_or_none()

        print(d.name)

        if not c:
            continue
        if d.code not in [dist.code for dist in c.districts]:
            c.districts.append(d)

    session.commit()

    # Update organization
    orgs = kwargs.get('orgs', '')
    for org in orgs:
        o = Organization()
        o.name = org.get('org_name', '')
        o.address = org.get('org_address', '')
        o.contact = org.get('org_contact', '')
        o.phone = org.get('org_phone', '')

        try:
            c = session.query(District).filter(
                District.code == org['org_district_code'][:5]).one_or_none()

            if not session.query(Organization.name).filter(Organization.name == o.name).one_or_none():
                c.organizations.append(o)
        except KeyError:
            if not session.query(Organization.name).filter(Organization.name == o.name).one_or_none():
                session.merge(o)
        print(o.name)

    session.commit()

    # Update rcbin
    rc_bins = kwargs.get('rc_bins', '')
    for rc_bin in rc_bins:
        r = RcBin()
        r.official_sn = rc_bin.get('official_sn', '')
        r.village = rc_bin.get('village', '')
        r.address = rc_bin.get('address', '')
        r.addr_with_dirs = rc_bin.get('addr_with_dirs', '')
        r.directions = rc_bin.get('directions', '')
        r.coords_lat = rc_bin.get('coords_lat', '')
        r.coords_lng = rc_bin.get('coords_lng', '')
        r.updated_on = rc_bin.get('updated_on', '')
        r.note = rc_bin.get('note', '')

        print(r.addr_with_dirs)
        try:
            d = session.query(District).filter(
                District.code == rc_bin['district_code']).one_or_none()

            if d:
                if not session.query(RcBin.addr_with_dirs).filter(RcBin.addr_with_dirs == r.addr_with_dirs).one_or_none():
                    d.rcbins.append(r)
        except KeyError:
            if not session.query(RcBin.addr_with_dirs).filter(RcBin.addr_with_dirs == r.addr_with_dirs).one_or_none():
                session.merge(r)

        try:
            o = session.query(Organization).filter(
                Organization.name == rc_bin['organization']['org_name']).one_or_none()

            if o:
                rc_bin_in_db = session.query(RcBin).filter(
                    RcBin.addr_with_dirs == r.addr_with_dirs).one_or_none()
                if rc_bin_in_db:
                    o.rcbins.append(rc_bin_in_db)
        except KeyError:
            pass

        session.commit()

    session.close()


if __name__ == '__main__':
    sources = read_sources()

    rc_bins_list = []
    orgs_list = []

    for source in sources:
        if source['name'] in skip_list:
            continue

        if not source['type']:
            continue
        elif source['type'][-3:] == 'csv':
            parser = CsvParser(source)
        elif source['type'][-4:] == 'json':
            continue
        elif source['type'][-4:] == 'xlsx':
            continue
        elif source['type'][-3:] == 'pdf':
            parser = PdfParser(source)
        elif source['type'] == 'soup':
            continue

        rc_bins = parser.get_rc_bins()
        if not rc_bins:
            print(
                f'{Fore.MAGENTA}[Failed to parse RcBins from {source["name"]}]{Fore.RESET}')
        else:
            pprint(rc_bins[:5])
            print(
                f'{Fore.MAGENTA}[Successfuly parsed {len(rc_bins)} RcBins from {source["name"]}]{Fore.RESET}')

        rc_bins_list += parser.rc_bins
        orgs_list += parser.organizations

    push_to_db(rc_bins=rc_bins_list, orgs=orgs_list)
