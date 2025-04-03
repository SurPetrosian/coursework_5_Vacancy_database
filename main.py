from time import sleep

from Vacancy_database.src.companies_search import HeadHunterCompanies
from Vacancy_database.src.db_manager import DBManager
from Vacancy_database.src.vacancies_search import HeadHunterVacancies

MY_COMPANIES_LIST = [
    "EasyCode",
    "ZUZEX",
    "Doubletapp",
    "SkillsRock",
    "DDoS-Guard",
    "Digital Sail",
    "Skillline",
    "Mindbox",
    "emi",
    "Voximplant",
]


def initial_setup() -> list:
    print("Добро пожаловать! Давайте начнем и настроем свой инструмент.\n")

    user_company_list = input(
        f"""Пожалуйста, введите имена компаний, вы хотели бы искать их открытые вакансии
или просто нажмите Enter, чтобы использовать список компаний по умолчанию. (По умолчанию: {MY_COMPANIES_LIST}\n"""
    )

    if user_company_list:
        companies_list = user_company_list.split(",")
    else:
        companies_list = MY_COMPANIES_LIST
    return companies_list


def parsing_companies(companies_list: list) -> list:
    companies_parser = HeadHunterCompanies(companies_list)

    companies_parser.prepare_to_fetch()

    companies_parser.get_companies_info()

    companies_parser.get_companies_id()

    return companies_parser.id_list


def parsing_vacancies(companies_id_list: list) -> list:
    vacancies_parser = HeadHunterVacancies()

    vacancies_parser.fetch_vacancies(companies_id_list)

    filtered_data = vacancies_parser.filter_data()

    return filtered_data


def setting_up_database(user_name: str, password: str) -> DBManager:
    db_manager = DBManager(user_name, password)

    db_manager.create_database()

    return db_manager


def set_database_option(option_number: str, database: DBManager) -> bool:
    app_status = True
    if option_number == "1":
        database.get_all_vacancies()
    elif option_number == "2":
        database.get_companies_and_vacancies_count()
    elif option_number == "3":
        database.get_avg_salary()
    elif option_number == "4":
        database.get_vacancies_with_higher_salary()
    elif option_number == "5":
        user_keyword = input("Пожалуйста, введите свое ключевое слово: \n")
        database.get_vacancies_with_keyword(user_keyword)
    elif option_number == "0":
        app_status = False
    else:
        print("Не могу распознать ваш выбор. Пожалуйста, попробуйте еще раз.\n")
    if app_status is True:
        print("\nВы можете продолжить работу или выйти из приложения\n")
    return app_status


def main() -> None:
    companies_list = initial_setup()

    print("Отлично! Теперь пришло время установить связь с вашей базой данных PostgreSQL\n")

    user_name = input("Пожалуйста, введите свое имя пользователя PostgreSQL: ")
    password = input("Пожалуйста, введите свой пароль: ")
    db_manager = setting_up_database(user_name, password)
    sleep(1)

    print("Все в порядке! Инициируя поиск в HeadHunter...\n")
    sleep(2)

    companies_id = parsing_companies(companies_list)
    sleep(2)
    vacancies = parsing_vacancies(companies_id)
    sleep(2)

    db_manager.fill_up_tables(companies_list, vacancies)
    print("Поиск завершен, а ваша база данных готова! Теперь вы можете выбрать номер опции для работы с вакансиями.\n")
    sleep(2)
    running_app = True
    while running_app:
        user_choice = input(
            """
        1. Посмотреть все доступные вакансии и их соответствующих работодателей.
        2. Посмотреть, сколько вакансий у каждого работодателя.
        3. Посмотреть  Среднюю зарплату среди всех доступных вакансий.
        4. Посмотреть Вакансии с зарплатой, большей, чем в среднем.
        5. Посмотреть Вакансии, отфильтрованные ключевым словом.
        0. Выйдите из приложения.\n"""
        )

        running_app = set_database_option(user_choice, db_manager)
        sleep(3)

    print("Закончить работу. Спасибо!")
    input("\n\n\nНажмите ENTER, чтобы выйти.")


if __name__ == "__main__":
    main()
