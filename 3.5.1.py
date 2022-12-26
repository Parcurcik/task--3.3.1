import pandas as pd
import sqlite3



df = pd.read_csv('currency_by_month.csv')

db = sqlite3.connect('currency.sqlite3')
make_cursor = db.cursor()
make_cursor.execute(
    'CREATE TABLE IF NOT EXISTS currency (date text, USD float, EUR float, KZT float, UAH float, BYR float)')
db.commit()
df.to_sql('currency', db, if_exists='replace', index=False)
make_cursor.execute('SELECT * FROM currency')
for row in make_cursor.fetchmany(10):
    print(row)

db.close()