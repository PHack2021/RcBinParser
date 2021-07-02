from typing import TypedDict


class Organization(TypedDict):
    uuid: str
    org_name: str
    org_address: str
    org_contact: str
    org_phone: str
    org_district: str
    org_district_code: str


class RcBin(TypedDict):
    uuid: str
    official_sn: str
    county_city: str
    district: str
    district_code: str
    village: str
    address: str
    addr_with_dirs: str
    directions: str
    organization: Organization  # delete this after _get_unique_organizations
    organization_uuid: str
    coords_lat: str
    coords_lng: str
    updated_on: str
    note: str
