import math
import sqlite3

import pandas as pd
from datetime import datetime
from dateutil import rrule
import xml.etree.ElementTree as ET
from urllib.request import urlopen
import divide_csv_file


def get_currency_dynamic(file_name):
    pd.set_option('expand_frame_repr', False)
    df = pd.read_csv(file_name)
    df = df.dropna(subset=['salary_from', 'salary_to'], how='all')
    df['currency_count'] = df.groupby('salary_currency')['salary_currency'].transform('count')
    df = df[df['currency_count'] > 5000]
    return df


def get_currency_dynamic_csv(file_name, dynamic_file_name):
    df = get_currency_dynamic(file_name)
    print(df['salary_currency'].value_counts())
    currencies = df['salary_currency'].unique()
    currencies = currencies[currencies != 'RUR']
    start_date = datetime.strptime(df['published_at'].min(), '%Y-%m-%dT%H:%M:%S%z').replace(day=28, hour=12, minute=0,
                                                                                            second=0)
    end_date = datetime.strptime(df['published_at'].max(), '%Y-%m-%dT%H:%M:%S%z').replace(day=28, hour=12, minute=0,
                                                                                          second=0)

    currency_dynamic = {key: [] for key in currencies}
    currency_dynamic['date'] = []
    for dt in rrule.rrule(rrule.MONTHLY, dtstart=start_date, until=end_date):
        tree = ET.parse(
            urlopen(f'http://www.cbr.ru/scripts/XML_daily.asp?date_req=28/{dt.strftime("%m/%Y")}d=1'))
        root = tree.getroot()
        for child in root.findall('Valute'):
            code = child.find('CharCode').text
            if code in currencies:
                if dt.strftime('%Y-%m') not in currency_dynamic['date']:
                    currency_dynamic['date'] += [dt.strftime('%Y-%m')]
                coeff = float(child.find('Value').text.replace(',', '.')) / float(child.find('Nominal').text)
                currency_dynamic[code] += [coeff]
        for key in currency_dynamic.keys():
            if key != 'date' and len(currency_dynamic['date']) > len(currency_dynamic[key]):
                currency_dynamic[key] += ['NaN']
    currency_df = pd.DataFrame(data=currency_dynamic)
    cols = currency_df.columns.tolist()
    cols = cols[-1:] + cols[:-1]
    currency_df = currency_df[cols]
    currency_df.to_csv(dynamic_file_name, index=False)


def convert_salary_to_rub(file_name):
    def convert_to_rub(row):
        if row['salary_currency'] != 'RUR':
            date = datetime.strptime(row['published_at'], '%Y-%m-%dT%H:%M:%S%z')
            df = pd.read_csv(f'csv_files/year_{date.year}.csv')
            convert_value = df[df['date'] == date.strftime('%Y-%m')][row['salary_currency']].values[0]
            return 'NaN' if math.isnan(convert_value) else row['salary'] * convert_value
        return row['salary']

    def count_salary(row):
        if math.isnan(row['salary_from']):
            return row['salary_to']
        elif math.isnan(row['salary_to']):
            return row['salary_from']
        return (row['salary_from'] + row['salary_to']) / 2

    dynamic_file_name = 'currency_by_month.csv'
    df = get_currency_dynamic(file_name)
    get_currency_dynamic_csv(file_name, dynamic_file_name)
    divide_csv_file.divide_currency_file_by_year(dynamic_file_name)
    # df = df.head(1000)
    df['salary'] = df.apply(count_salary, axis=1)
    df['salary'] = df.apply(convert_to_rub, axis=1)
    df = df[df['salary'] != 'NaN']
    df.head(100).loc[:, ['name', 'salary', 'area_name', 'published_at']].to_csv('salary_info.csv', index=False)
    return df.loc[:, ['name', 'salary', 'area_name', 'published_at']]

def convert_salary_to_rub_sqlite(file_name):
    def convert_to_rub(row):
        if row['salary_currency'] != 'RUR':
            date = datetime.strptime(row['published_at'], '%Y-%m-%dT%H:%M:%S%z').strftime('%Y-%m')
            convert_value = c.execute(f"SELECT {row['salary_currency']} FROM currency_dynamic WHERE date = '{date}'").fetchone()[0]
            return None if not convert_value else row['salary'] * convert_value
        return row['salary']

    def count_salary(row):
        if math.isnan(row['salary_from']):
            return row['salary_to']
        elif math.isnan(row['salary_to']):
            return row['salary_from']
        return (row['salary_from'] + row['salary_to']) / 2

    conn = sqlite3.connect('currency.sqlite3')
    c = conn.cursor()
    df = get_currency_dynamic(file_name)
    df['salary'] = df.apply(count_salary, axis=1)
    df['salary'] = df.apply(convert_to_rub, axis=1)
    df = df[df['salary'] != 'NaN']
    df['published_at'] = df.apply(lambda row: datetime.strptime(row['published_at'], '%Y-%m-%dT%H:%M:%S%z').strftime('%Y-%m-%d'), axis = 1)
    conn = sqlite3.connect('aboutSalaries.sqlite3')
    c = conn.cursor()
    c.execute(
        'CREATE TABLE IF NOT EXISTS salary_info (name text, salary float, area_name text, published_at date)')
    conn.commit()
    df.loc[:, ['name', 'salary', 'area_name', 'published_at']].to_sql('salary_info', conn, if_exists='replace', index=False)
    c.execute('SELECT * FROM salary_info')
    conn.close()

convert_salary_to_rub_sqlite('vacancies_dif_currencies.csv')