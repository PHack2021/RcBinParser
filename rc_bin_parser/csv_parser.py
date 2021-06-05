import csv
import re
from typing import List

from requests.models import Response

from .base_parser import BaseParser
from .data_types import Organization, RcBin


class CsvParser(BaseParser):

    def _cleanup_resource(self, resource: str):
        return re.sub(r'[\n]+["]', '\"', resource)

    def _get_csv_from_resource(self, resource: Response) -> list:
        encoding = self.source.get('encoding', 'UTF-8')
        rc_bins_raw = resource.content.decode(encoding)
        rc_bins_raw = self._cleanup_resource(rc_bins_raw)

        rc_bins_csv = list(csv.reader(rc_bins_raw.splitlines()))

        has_headers = bool(self.source.get('has_headers', 'True'))
        if has_headers:
            del rc_bins_csv[0]

        return rc_bins_csv

    def _parse_rc_bins_from_resource(self, resource: Response) -> List[RcBin]:
        rc_bins_csv = self._get_csv_from_resource(resource)

        column_names = self.source['columns'].split()
        rc_bins = []

        for row in rc_bins_csv:
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
