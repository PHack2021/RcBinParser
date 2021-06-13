import csv
import re
from typing import List

from requests.models import Response

from .base_parser import BaseParser


class CsvParser(BaseParser):

    def _cleanup_resource(self, resource: str):
        return re.sub(r'[\n]+["]', '\"', resource)

    def _get_list_from_resource(self, resource: Response) -> list:
        encoding = self.source.get('encoding', 'UTF-8')
        rc_bins_raw = resource.content.decode(encoding)
        rc_bins_raw = self._cleanup_resource(rc_bins_raw)

        rc_bins_csv = list(csv.reader(rc_bins_raw.splitlines()))

        has_headers = bool(self.source.get('has_headers', 'True'))
        if has_headers:
            del rc_bins_csv[0]

        return rc_bins_csv
