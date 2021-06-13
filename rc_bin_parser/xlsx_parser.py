from typing import List

from requests.models import Response

from .base_parser import BaseParser
from .data_types import RcBin


class XlsxParser(BaseParser):

    book = load_workbook('test.xlsx')
    sheet = book.active

    rows = sheet.rows

    def _parse_rc_bins_from_resource(self, resource: Response) -> List[RcBin]:
        rc_bins_xlsx = self._get_xlsx_from_resource(resource)

        column_names = self.source['columns']
        rc_bins = []


        for row in rc_bins_xlsx:
            rc_bin = RcBin()
            for name, value in zip(column_names, row):
                data[name] = value.value
            
            rc_bins.append(rc_bin)

        print(rc_bins)
