from abc import ABC, abstractmethod

import requests

from Vacancy_database.src.logger import general_logger


class BaseCompaniesParser(ABC):

    @abstractmethod
    def prepare_to_fetch(self):
        pass

    @abstractmethod
    def get_companies_info(self):
        pass


class HeadHunterCompanies(BaseCompaniesParser):
    """"Class-Connector to HH.Ru API для получения идентификации компаний по их именам"""

    companies_list: list

    def __init__(self, companies_list):
        self.__companies_list = companies_list
        self.__url = "https://api.hh.ru/employers"
        self.__headers = {"User-Agent": "HH-User-Agent"}
        self.__companies_name_id = []
        self.__id_list = []

    @property
    def url(self):
        return self.__url

    @property
    def headers(self):
        return self.__headers

    @property
    def companies_list(self):
        return self.__companies_list

    @property
    def companies_name_id(self):
        return self.__companies_name_id

    @property
    def id_list(self):
        return self.__id_list

    def prepare_to_fetch(self) -> None:
        """Создание словаря с названием компании и идентификатором"""
        for company in self.__companies_list:
            company_name_id = {"name": company, "id": None}
            self.__companies_name_id.append(company_name_id)

    def get_companies_info(self) -> None:
        """Получение идентификационного номера компании от HH API (только компании с активными вакансиями)"""
        for company in self.__companies_name_id:
            general_logger.info(f"Searching company: {company['name']}")
            response = requests.get(
                url=self.__url,
                headers=self.__headers,
                params={
                    "text": company["name"],
                    "page": 0,
                    "per_page": 100,
                    "only_with_vacancies": True,
                },
            )
            company_info = response.json()
            try:
                company["id"] = company_info["items"][0]["id"]
                general_logger.info(f"Found id: {company['id']} for {company['name']}")
            except IndexError:
                general_logger.info(f"Did not found id for {company['name']}")

    def get_companies_id(self) -> None:
        """Создание списка идентификатора компаний для дальнейшего поиска вакансий"""
        self.__id_list = [company["id"] for company in self.__companies_name_id]
