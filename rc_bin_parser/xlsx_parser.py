from typing import List

from requests.models import Response

from .base_parser import BaseParser
from .data_types import RcBin


class XlsxParser(BaseParser):

    def _parse_rc_bins_from_resource(self, resource: Response) -> List[RcBin]:
        pass
