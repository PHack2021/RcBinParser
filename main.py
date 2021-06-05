import json
from rc_bin_parser import CsvParser
from typing import List
from pprint import pprint


SOURCES_PATH = 'resources/sources.json'


def read_sources() -> List[dict]:
    with open(SOURCES_PATH, 'r') as f:
        sources = json.load(f)
    return sources


if __name__ == '__main__':
    sources = read_sources()

    for source in sources:
        if not source['type']:
            continue
        elif source['type'][-3:] == 'csv':
            parser = CsvParser(source)
        elif source['type'][-4:] == 'json':
            continue
        elif source['type'][-4:] == 'xlsx':
            continue
        elif source['type'][-3:] == 'pdf':
            continue
        elif source['type'] == 'soup':
            continue

        rc_bins = parser.get_rc_bins()
        if not rc_bins:
            print(f'[Failed to parse RcBins from {source["name"]}]')
        # pprint(rc_bins[:2])
        print(
            f'[Successfuly parsed {len(rc_bins)} RcBins from {source["name"]}]')
