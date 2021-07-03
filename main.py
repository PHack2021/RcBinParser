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
from models import District, County_City, Organization
from rc_bin_parser import CsvParser, PdfParser

from rc_bin_parser.utils import get_dict_from_csv

SOURCES_PATH = 'resources/sources.json'
skip_list = ['嘉義市', '新北市', '台南市', '高雄市']


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

        if not c:
            continue
        if d.code not in [dist.code for dist in c.districts]:
            c.districts.append(d)

    # Update organization
    organizations = kwargs.get('orgs', '')
    organizations = organizations.split('/')
    org_dist = kwargs.get('dists', '')
    org_dist = org_dist.split('/')
    for organization, dist in zip(organizations[:-1], org_dist[:-1]):
        organization = eval(organization)

        o = Organization()
        o.uuid = organization['uuid']
        o.name = organization['org_name']
        #o.address = organization['address']
        #o.contact = organization['contact']
        o.phone = organization['org_phone']

        if not d:
            continue
        for district in districts:
            if dist in district.values():
                o.district_code = district['code']

    session.commit()


if __name__ == '__main__':
    sources = read_sources()

    dist_str = ''
    org_str = ''

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

    for rc_bin in rc_bins:
        dist_str += str(rc_bin['district']) + '/'
        org_str += str(rc_bin['organization']) + '/'

    push_to_db(dists=dist_str, orgs=org_str)
