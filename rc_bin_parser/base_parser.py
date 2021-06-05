from typing import List, Any

import requests
from bs4 import BeautifulSoup

from .data_types import RcBin


class BaseParser():

    def __init__(self, source: dict):
        self.source = source

    @classmethod
    def _fetch_from_url(url: str, headers: dict = {}) -> requests.models.Response:
        try:
            r = requests.get(url, headers=headers)
        except:
            return False
        if r.status_code != 200:
            return False

        return r

    @classmethod
    def _get_soup(cls, url: str, headers: dict = {}) -> BeautifulSoup:
        r = cls._fetch_from_url(url, headers)
        return BeautifulSoup(r.text, 'lxml')

    @classmethod
    def _format_url(url: str, base_url: str) -> str:
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

        if self.source['type'][:3] is 'api':
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

    def _parse_rc_bins_from_resource(self) -> List[dict]:
        pass

    def get_rc_bins(self) -> List[dict]:
        url = self._get_resource_url()
        if not url:
            return False

        resource = self._get_resource(url)

        rc_bins = self._parse_rc_bins_from_resource()


class SoupParser(BaseParser):
    def _get_resource(self, resource_url):
        return self._get_soup(resource_url)

    def _get_resource_url(self) -> str:
        return self.source['url']


# class XlsxParser():
#     pass


# class PdfParser():
#     pass


# class JsonParser():
#     pass


# class XmlParser():
#     pass
