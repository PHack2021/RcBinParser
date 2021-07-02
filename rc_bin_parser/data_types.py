from typing import TypedDict


class Organization(TypedDict):
    uuid: str                   # PK <UUID>
    org_name: str               # <TEXT>
    org_address: str            # <TEXT>
    org_contact: str            # <TEXT>
    org_phone: str              # <TEXT>
    org_district: str
    org_district_code: str      # <TEXT>


class RcBin(TypedDict):
    uuid: str                   # PK <UUID>
    official_sn: str            # <TEXT>
    county_city: str
    district: str
    district_code: str          # <TEXT>
    village: str                # <TEXT>
    address: str                # <TEXT>
    addr_with_dirs: str         # <TEXT>
    directions: str             # <TEXT>
    organization: Organization
    organization_uuid: str      # FK <TEXT> organization->uuid
    coords_lat: str             # <TEXT>
    coords_lng: str             # <TEXT>
    updated_on: str             # <DATE>
    note: str                   # <TEXT>
