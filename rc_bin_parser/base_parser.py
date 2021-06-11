from abc import ABC, abstractmethod
from typing import Any, List

import requests
from bs4 import BeautifulSoup

from .data_types import RcBin

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
    def _parse_rc_bins_from_resource(self, resource: Any) -> List[RcBin]:
        raise NotImplementedError

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
        return self.rc_bins
