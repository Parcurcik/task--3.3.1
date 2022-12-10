currency_to_rub = {
    "AZN": 35.68, "BYR": 23.91, "EUR": 59.90, "GEL": 21.74, "KGS": 0.76,
    "KZT": 0.13, "RUR": 1, "UAH": 1.64, "USD": 60.66, "UZS": 0.0055,
}


class Vacancy:
    """
    Класс описывает сущность вакансии
    Атрибуты (все атрибуты имеют свойства)
    ------------------------------------------------------------------------
    __name: str
        Название вакансии
    __salary_from: float
        Нижняя граница оклада
    __salary_to: float
        Верхняя граница оклада
    __salary_currency: str
        Валюта оклада
    __area_name: str
        Название региона
    __published_at: str
        Дата публикации объявления
    Отдельные свойства
    ------------------------------------------------------------------------
    year: str
        Год публикации объявления
    average_ru_salary: float
        Средняя зарплата в рублях
    """
    def __init__(self, vacancy_dict):
        """
        Инициализирует объект
        :param vacancy_dict: {str: str}
            Входящий словарь со всей информацией для инициализации объекта
        """
        self.__name = vacancy_dict['name']
        self.__salary_from = float(vacancy_dict['salary_from'])
        self.__salary_to = float(vacancy_dict['salary_to'])
        self.__salary_currency = vacancy_dict['salary_currency']
        self.__area_name = vacancy_dict['area_name']
        self.__published_at = vacancy_dict['published_at']

    @property
    def name(self) -> str:
        return self.__name

    @name.setter
    def name(self, value: str):
        self.__name = value

    @property
    def salary_from(self) -> float:
        return self.__salary_from

    @salary_from.setter
    def salary_from(self, value: str):
        self.__salary_from = value

    @property
    def salary_to(self) -> float:
        return self.__salary_to

    @salary_to.setter
    def salary_to(self, value: str):
        self.__salary_to = value

    @property
    def salary_currency(self) -> str:
        return self.__salary_currency

    @salary_currency.setter
    def salary_currency(self, value: str):
        self.__salary_currency = value

    @property
    def area_name(self) -> str:
        return self.__area_name

    @area_name.setter
    def area_name(self, value: str):
        self.__area_name = value

    @property
    def published_at(self) -> str:
        return self.__published_at

    @published_at.setter
    def published_at(self, value: str):
        self.__published_at = value

    @property
    def year(self):
        return self.__published_at[0:4]

    @property
    def average_ru_salary(self):
        return (self.__salary_from + self.__salary_to) / 2 * currency_to_rub[self.__salary_currency]