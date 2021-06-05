from .base_parser import BaseParser
from bs4 import BeautifulSoup


class SoupParser(BaseParser):
    def _get_resource(self, resource_url) -> BeautifulSoup:
        return self._get_soup(resource_url)

    def _get_resource_url(self) -> str:
        return self.source['url']
