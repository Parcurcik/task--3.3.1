from concurrent import futures
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from jinja2 import Environment, FileSystemLoader
import pdfkit
from matplotlib import ticker


def start_processes(arguments):
    vac_name = arguments[0]
    year = arguments[1]
    pr_df = pd.read_csv(f'created_csv_files\\part_{year}.csv')

    pr_df.loc[:, 'salary'] = pr_df.loc[:, ['salary_from', 'salary_to']].mean(axis=1)

    pr_df_vac = pr_df[pr_df["name"].str.contains(vac_name)]

    s_by_year, v_by_year, inp_v_s, inp_v_c = {year: []}, {year: 0}, {year: []}, {year: 0}

    s_by_year[year] = int(pr_df['salary'].mean())
    v_by_year[year] = len(pr_df)
    inp_v_s[year] = int(pr_df_vac['salary'].mean())
    inp_v_c[year] = len(pr_df_vac)

    d_list = [s_by_year, v_by_year, inp_v_s, inp_v_c]
    return d_list


if __name__ == "__main__":
    def sort_dict(dictionary):
        sorted_dict = {}
        for key in sorted(dictionary):
            sorted_dict[key] = dictionary[key]
        return sorted_dict


    def sort_area_dict(dictionary):
        sorted_tuples = sorted(dictionary.items(), key=lambda item: item[1], reverse=True)[:10]
        sorted_dict = {k: v for k, v in sorted_tuples}
        return sorted_dict


    class UserInput:
        def __init__(self):
            self.file_name = input("Введите название файла: ")
            self.vacancy_name = input("Введите название профессии: ")


    class MakeCvs:
        def __init__(self, file_name):
            self.dataframe = pd.read_csv(file_name)

            self.dataframe["years"] = self.dataframe["published_at"].apply(
                lambda date: int(".".join(date[:4].split("-"))))
            self.years = list(self.dataframe["years"].unique())

            for year in self.years:
                data = self.dataframe[self.dataframe["years"] == year]
                data[["name", "salary_from", "salary_to",
                      "salary_currency", "area_name",
                      "published_at"]].to_csv(f"created_csv_files\\part_{year}.csv", index=False)


    class Report:
        rows_by_year = ["Год", "Средняя зарплата", "Средняя зарплата - ", "Количество вакансий",
                        "Количество вакансий - "]

        def __init__(self, vac_name, dicts_by_year):
            self.generate_image(vac_name, dicts_by_year)
            self.generate_pdf(vac_name, dicts_by_year)

        @staticmethod
        def generate_pdf(vac_name, dicts_by_year):
            env = Environment(loader=FileSystemLoader('.'))
            template = env.get_template("pdf_template.html")

            pdf_template = template.render(
                {'name': vac_name, 'by_year': dicts_by_year})

            options = {'enable-local-file-access': None}
            config = pdfkit.configuration(wkhtmltopdf=r'C:\Program Files\wkhtmltopdf\bin\wkhtmltopdf.exe')
            pdfkit.from_string(pdf_template, 'report.pdf', configuration=config, options=options)

        @staticmethod
        def generate_image(vac_name, dicts_by_year):
            x_nums = np.arange(len(dicts_by_year[0].keys()))
            width = 0.4
            x_list1 = x_nums - width / 2
            x_list2 = x_nums + width / 2
            fig = plt.figure()

            ax = fig.add_subplot(221)
            ax.set_title("Уровень зарплат по годам")
            ax.bar(x_list1, dicts_by_year[0].values(), width, label="средняя з/п")
            ax.bar(x_list2, dicts_by_year[1].values(), width, label=f"з/п {vac_name.lower()}")
            ax.set_xticks(x_nums, dicts_by_year[0].keys(), rotation="vertical")
            ax.tick_params(axis="both", labelsize=8)
            ax.legend(fontsize=8)
            ax.grid(True, axis="y")

            ax = fig.add_subplot(222)
            ax.set_title("Количество вакансий по годам")
            ax.bar(x_list1, dicts_by_year[2].values(), width, label="Количество вакансий")
            ax.bar(x_list2, dicts_by_year[3].values(), width, label=f"Количество вакансий \n{vac_name.lower()}")
            ax.set_xticks(x_nums, dicts_by_year[2].keys(), rotation="vertical")
            ax.tick_params(axis="both", labelsize=8)
            ax.legend(fontsize=8)
            ax.grid(True, axis="y")

            plt.tight_layout()
            plt.savefig("graph.png")


    inputed = UserInput()
    file, vac = inputed.file_name, inputed.vacancy_name
    make_csv = MakeCvs(file)
    df = make_csv.dataframe
    years = make_csv.years

    df["published_at"] = df["published_at"].apply(lambda date: int(".".join(date[:4].split("-"))))
    df['salary'] = df.loc[:, ['salary_from', 'salary_to']].mean(axis=1)

    salaries_by_year, vacancies_by_year, inp_vacancy_salary, inp_vacancy_count = {}, {}, {}, {}

    executor = futures.ProcessPoolExecutor()
    processes = []
    for year in years:
        args = (vac, year)
        returned_list = executor.submit(start_processes, args).result()
        salaries_by_year.update(returned_list[0])
        vacancies_by_year.update(returned_list[1])
        inp_vacancy_salary.update(returned_list[2])
        inp_vacancy_count.update(returned_list[3])

    print("Динамика уровня зарплат по годам:", sort_dict(salaries_by_year))
    print("Динамика количества вакансий по годам:", sort_dict(vacancies_by_year))
    print("Динамика уровня зарплат по годам для выбранной профессии:", sort_dict(inp_vacancy_salary))
    print("Динамика количества вакансий по годам для выбранной профессии:", sort_dict(inp_vacancy_count))

    dicts_list_by_year = [sort_dict(salaries_by_year), sort_dict(vacancies_by_year),
                          sort_dict(inp_vacancy_salary), sort_dict(inp_vacancy_count)]

    report = Report(inputed.vacancy_name, dicts_list_by_year)