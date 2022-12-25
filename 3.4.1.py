import math
from statistics import mean
import pandas as pd

pd.set_option("expand_frame_repr", False)
df = pd.read_csv("vacancies_dif_currencies.csv")
df_date = pd.read_csv("currency_by_month.csv")


def get_salary(s_from, s_to, s_cur, date):
    date = date[1] + "/" + date[0]
    s_cur_value = 0

    if s_cur != "RUR" and (s_cur == s_cur) and s_cur in ["BYN", "BYR", "EUR", "KZT", "UAH", "USD"]:
        s_cur.replace("BYN", "BYR")
        df_date_row = df_date.loc[df_date["date"] == date]
        s_cur_value = df_date_row[s_cur].values[0]
    elif s_cur == "RUR":
        s_cur_value = 1

    if math.isnan(s_from) and not (math.isnan(s_to)):
        return s_to * s_cur_value
    elif not (math.isnan(s_from)) and math.isnan(s_to):
        return s_from * s_cur_value
    elif not (math.isnan(s_from)) and not (math.isnan(s_to)):
        return mean([s_from, s_to]) * s_cur_value


df["salary"] = df.apply(lambda row: get_salary(row["salary_from"], row["salary_to"], row["salary_currency"],
                                               row["published_at"][:7].split("-")), axis=1)

df[:100].to_csv("info_about_salarys.csv", index=False)