from abc import ABC, abstractmethod
from typing import Any, List

import requests
from bs4 import BeautifulSoup

from .data_types import RcBin, Organization

UA = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.169 Safari/537.36'


class BaseParser(ABC):
    rc_bins = []
    source = None

    def __init__(self, source: dict):
        self.source = source

    @classmethod
    def _fetch_from_url(cls, url: str, headers: dict = {'user-agent': UA}) -> requests.models.Response:
        try:
            r = requests.get(url, headers=headers, timeout=5)
        except:
            return False
        if r.status_code != 200:
            print(f'[fetch_from_url failed: {r.status_code}]')
            return False

        return r

    @classmethod
    def _get_soup(cls, url: str, headers: dict = {}) -> BeautifulSoup:
        r = cls._fetch_from_url(url, headers)
        return BeautifulSoup(r.text, 'lxml')

    @classmethod
    def _format_url(cls, url: str, base_url: str) -> str:
        if url.startswith('//'):
            return f'https:{url}'

        elif url.startswith('/') or url:
            base_url = requests.compat.urlparse(base_url)
            base_url = f'{base_url.scheme}://{base_url.netloc}'

            return requests.compat.urljoin(base_url, url)
        else:
            return ''

    def _get_resource_url(self) -> str:
        url = self.source['url']

        if self.source['type'][:3] == 'api':
            return url
        else:
            soup = self._get_soup(url)
            resource_element = soup.select_one(
                self.source['resource_selector'])
            if not resource_element:
                return False
            resource_url = self._format_url(
                resource_element['href'], url)
            return resource_url

    def _get_resource(self, resource_url: str) -> Any:
        return self._fetch_from_url(resource_url)

    # Implement for parsers for different data types
    @abstractmethod
    def _get_list_from_resource(self, resource: requests.models.Response) -> list:
        raise NotImplementedError

    # def _split_addr_with_dirs(self):
    #     if not self.rc_bins:
    #         return
        # addr_pattern = r'[.*][縣｜市]'

        # for rc_bin in self.rc_bins:
        #     if

    def _get_unique_organizations(self) -> List[Organization]:
        # get unique organizations and generate uuid, then delete Organization in rcbins and point to correct organization_uuid
        pass

    def _parse_rc_bins_from_resource(self, resource: Any) -> List[RcBin]:
        rc_bins_raw = self._get_list_from_resource(resource)

        column_names = self.source['columns']
        rc_bins = []

        for row in rc_bins_raw:
            rc_bin = RcBin()
            org = Organization()

            for name, value in zip(column_names, row):
                if 'org' in name:
                    org[name] = value
                    continue
                rc_bin[name] = value

            if org:
                rc_bin['organization'] = org

            rc_bins.append(rc_bin)

        return rc_bins

    # Main Entry Point
    def get_rc_bins(self) -> List[RcBin]:
        url = self._get_resource_url()
        if not url:
            print('[Failed to get resource_url]')
            return False

        resource = self._get_resource(url)
        if not resource:
            print('[Failed to get resource]')
            return False

        self.rc_bins = self._parse_rc_bins_from_resource(resource)

        self.organizations = self._get_unique_organizations()
        return self.rc_bins
