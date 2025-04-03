from abc import ABC, abstractmethod

import requests

from Vacancy_database.src.logger import general_logger


class BaseVacancyParser(ABC):

    @abstractmethod
    def fetch_vacancies(self, employers_info):
        pass

    @abstractmethod
    def filter_data(self):
        pass


class HeadHunterVacancies(BaseVacancyParser):
    """Класс-подключение к HH.RU API для получения открытых вакансий желаемых компаний"""

    def __init__(self):
        self.__url = "https://api.hh.ru/vacancies"
        self.__headers = {"User-Agent": "HH-User-Agent"}
        self.__params = {"text": "", "page": 0, "per_page": 100}
        self.vacancies = []

    @property
    def url(self):
        return self.__url

    @property
    def headers(self):
        return self.__headers

    @property
    def params(self):
        return self.__params

    def fetch_vacancies(self, employers_id: list) -> None:

        general_logger.info("Searching vacancies")
        response = requests.get(
            self.__url,
            headers=self.__headers,
            params={"page": 0, "per_page": 100, "employer_id": employers_id},
        )
        if response.status_code == 200:
            vacancies = response.json()["items"]
            self.vacancies.extend(vacancies)
            general_logger.info("Vacancies successfully added to list")

    def filter_data(self) -> list:

        filtered_data = []
        for vacancy in self.vacancies:
            try:
                if vacancy.get("salary").get("currency") == "RUR":
                    current_vacancy = dict()
                    current_vacancy["name"] = vacancy["name"]
                    current_vacancy["salary"] = vacancy.get("salary")
                    current_vacancy["url"] = vacancy["alternate_url"]
                    current_vacancy["experience"] = vacancy["experience"]["name"]
                    current_vacancy["employer"] = vacancy["employer"]["name"]
                    del current_vacancy["salary"]["gross"]
                    filtered_data.append(current_vacancy)
            except AttributeError:
                continue
        return filtered_data
