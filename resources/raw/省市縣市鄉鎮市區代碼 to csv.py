# %%
import csv
import re
from pprint import pprint


with open('省市縣市鄉鎮市區代碼.txt') as f:
    data = f.readlines()

to_exclude = [
    '兵役協會',
    '內政部入出國及移民署',
    '逕為登記',
    '資料補登',
    '國外',
    '補辦戶籍遷入',
    '取得國籍遷入',
    '註銷外僑登記',
    '自大陸地區遷入',
    '兵役處',
    '中華民國內政部',
    '民政處',
    '民政局',
    '臺北縣',
    '桃園縣',
    '台中縣',
    '台南縣',
    '高雄縣',
    '臺中縣',
]
exclude_list = re.compile('|'.join(to_exclude))

districts = []
for entry in data:
    district_code, district_name = entry.strip().split('=')
    district_name = re.sub(r'(臺灣省|福建省)', '', district_name)

    if exclude_list.search(district_name):
        continue

    if len(district_name) == 3:
        continue

    if not district_name:
        continue

    county_city = district_name[:3]
    district_name = district_name[3:]

    district = {
        'name': district_name,
        'code': district_code,
        'county_city': county_city
    }
    districts.append(district)

print(districts)

with open('districts.csv', 'w') as f:
    writer = csv.DictWriter(f, districts[0].keys())
    writer.writeheader()
    writer.writerows(districts)
    f.close()
