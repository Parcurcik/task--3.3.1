import math
from statistics import mean
import pandas as pd

pd.set_option("expand_frame_repr", False)
file = 'vacancies_dif_currincies'
df = pd.read_csv(file)
df_currency_from_api = pd.read_csv("final_currency.csv")


def set_salary_with_cur(salary_from, salary_to, currency, published_at):
    published_at = published_at[1] + "/" + published_at[0]
    currency_value = 0

    if currency != "RUR" and (currency == currency):
        if currency in ["BYN", "BYR", "EUR", "KZT", "UAH", "USD"]:
            currency = "BYR" if currency == "BYN" else currency
            df_currency_from_api_row = df_currency_from_api.loc[df_currency_from_api["date"] == published_at]
            currency_value = df_currency_from_api_row[currency].values[0]
    elif currency == "RUR":
        currency_value = 1

    return check_conditions(salary_from, salary_to, currency_value)


def check_conditions(salary_from, salary_to, currency_value):
    from_nan = math.isnan(salary_from)
    to_nan = math.isnan(salary_to)

    if from_nan and not to_nan:
        return salary_to * currency_value
    elif not from_nan and to_nan:
        return salary_from * currency_value
    elif not from_nan and not to_nan:
        return mean([salary_from, salary_to]) * currency_value


df["salary"] = df.apply(lambda row: set_salary_with_cur(row["salary_from"], row["salary_to"], row["salary_currency"],
                                                        row["published_at"][:7].split("-")), axis=1)

df[:100].to_csv("top_100.csv", index=False)