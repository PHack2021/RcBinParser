import csv


def get_dict_from_csv(path: str):
    with open(path, 'r', encoding='UTF-8') as f:
        reader = csv.DictReader(f)
        csv_content = list(reader)
    return csv_content
