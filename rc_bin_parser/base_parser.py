import json
from typing import Dict, List

import requests
from bs4 import BeautifulSoup

from .rc_bin import RcBin


class BaseParser():

    def __init__(self, source: dict):
        self.source = source

    @classmethod
    def _get_soup(url: str, headers: dict = {}) -> BeautifulSoup:
        try:
            r = requests.get(url, headers=headers)
        except:
            return False

        if r.status_code != 200:
            return False

        return BeautifulSoup(r.text, 'lxml')

    def get_rc_bin_data() -> list[Dict]:
        pass
