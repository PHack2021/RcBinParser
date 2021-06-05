from typing import TypedDict


class Organization(TypedDict):
    org_name: str
    org_address: str
    org_contact: str
    org_phone: str
    org_district: str
    org_district_code: str


class RcBin(TypedDict):
    official_sn: str
    county_city: str
    district: str
    district_code: str
    village: str
    address: str
    addr_with_dirs: str
    directions: str
    organization: Organization
    coords_lat: str
    coords_lng: str
    updated_on: str
    note: str
