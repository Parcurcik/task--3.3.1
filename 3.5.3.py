import sqlite3
import pandas as pd

vacancy = 'Программист'
conn = sqlite3.connect('bd.sqlite3')
c = conn.cursor()
df = pd.read_sql_query("SELECT strftime('%Y', published_at) as year, ROUND(AVG(salary), 4) as average_salary FROM salary_info GROUP BY strftime('%Y', published_at)", conn)
print(df)
df = pd.read_sql_query("SELECT  strftime('%Y', published_at) as year, COUNT(name) as vacancies_number FROM salary_info GROUP BY strftime('%Y', published_at)", conn)
print(df)
df = pd.read_sql_query(f"SELECT  strftime('%Y', published_at) as year, COUNT(name) as vacancies_number FROM salary_info WHERE name LIKE '%{vacancy}%' GROUP BY strftime('%Y', published_at)", conn)
print(df)
df = pd.read_sql_query(f"SELECT  strftime('%Y', published_at) as year, COUNT(name) as vacancies_number FROM salary_info WHERE name LIKE '%{vacancy}%' GROUP BY strftime('%Y', published_at)", conn)
print(df)
all_vacancies = c.execute('SELECT COUNT(*) FROM salary_info').fetchone()[0]
df = pd.read_sql_query(f"SELECT  area_name as city, ROUND(AVG(salary),4) as salary FROM salary_info GROUP BY area_name HAVING COUNT(name) >= {all_vacancies} / 100 ORDER BY AVG(salary) DESC LIMIT 10", conn)
print(df)
df = pd.read_sql_query(f"SELECT  area_name as city, ROUND(CAST(COUNT(name) AS FLOAT) / {all_vacancies},4) as share FROM salary_info GROUP BY area_name HAVING COUNT(name) >= {all_vacancies} / 100 ORDER BY COUNT(name) / {all_vacancies} DESC LIMIT 10", conn)
print(df)