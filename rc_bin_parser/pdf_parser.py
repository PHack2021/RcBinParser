from io import BytesIO
from typing import List

import pdfplumber
from requests.models import Response

from .base_parser import BaseParser
from .data_types import Organization, RcBin


class PdfParser(BaseParser):

    def _get_pdf_from_resource(self, resource: Response) -> list:
        rc_bins_pdf = []

        has_headers = self.source.get('has_headers', 'True')
        # 'AllPages' : 1 header row on each page
        # 'True'     : 1 header row at the start
        # 'False     : 0 header rows

        pdf = pdfplumber.open(BytesIO(resource.content))
        for page in pdf.pages:
            table = page.extract_table()

            if has_headers == 'AllPages':
                del table[0]
            rc_bins_pdf += table

        if has_headers == 'True':
            del rc_bins_pdf[0]

        return rc_bins_pdf

    def _parse_rc_bins_from_resource(self, resource: Response) -> List[RcBin]:
        rc_bins_pdf = self._get_pdf_from_resource(resource)

        column_names = self.source['columns']
        rc_bins = []

        for row in rc_bins_pdf:
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
