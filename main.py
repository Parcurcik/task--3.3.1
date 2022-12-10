import pandas as pd
from _datetime import datetime
from xml.etree import ElementTree
import numpy as np
import grequests
import requests
import datetime as DT

file_name = "vacancies_new.csv"

for date in dates:
    t = pd.to_datetime(str(date))
    timestring = t.strftime('%d/%m/%Y')
    data_dict["date"].append(t.strftime('%Y-%m'))
    sites.append(rf"http://www.cbr.ru/scripts/XML_daily.asp?date_req={timestring}")

response = (grequests.get(url) for url in sites)
for res in grequests.map(response):
    data = {}
    root = ElementTree.fromstring(res.content)
    for element in root.iter('Valute'):
        args = []
        for child in element:
            args.append(child.text)
        if headers.__contains__(args[1]):
            data[args[1]] = round(float(args[4].replace(',', '.')) / int(args[2]), 6)
    for key in headers:
        if data_dict.__contains__(key):
            data_dict[key].append(data_dict[key])
        else:
            data_dict[key].append(0)

df = pd.DataFrame(data_dict)
df.to_csv("dataframe.csv", index=False)