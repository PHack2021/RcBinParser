from dataclasses import dataclass


@dataclass
class Organization:
    organization_name: str
    organization_address: str
    organization_contactL: str
    organization_phone: str


@dataclass
class RcBin:
    county_city: str
    district: str
    district_code: str
    community: str
    address: str
    address_w_directions: str
    directions: str
    organization: Organization
    coordinates: tuple(str, str)
    updated_on: str
    note: str
