from typing import List

from bs4 import BeautifulSoup

from .base_parser import BaseParser
from .data_types import RcBin


class SoupParser(BaseParser):
    def _get_resource(self, resource_url) -> BeautifulSoup:
        return self._get_soup(resource_url)

    def _get_resource_url(self) -> str:
        return self.source['url']

    def _parse_rc_bins_from_resource(self, soup: BeautifulSoup) -> List[RcBin]:
        for resource in self.source['resources']:
            elements = soup.select(resource['selector'])

            for element in elements:
                pass
