import csv


def get_dict_from_csv(path: str):
    with open(path, 'r') as f:
        reader = csv.DictReader(f)
        csv_content = list(reader)
    return csv_content
