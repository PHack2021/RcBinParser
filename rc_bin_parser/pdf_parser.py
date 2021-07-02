from io import BytesIO
from typing import List

import pdfplumber
from requests.models import Response

from .base_parser import BaseParser


class PdfParser(BaseParser):

    def _get_list_from_resource(self, resource: Response) -> list:
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
