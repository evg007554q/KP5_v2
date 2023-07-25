from configparser import ParsingError
import requests

from db_manager import DBManager


def get_request(url,  params):
    headers = {
        "User_Agent": "MyImportantApp 1.0"
    }
    response = requests.get(url, headers=headers, params=params)

    if response.status_code != 200:
        raise ParsingError(f'Ошибка подключения к hh.ru! Статус:{response.status_code}')
    return response.json()["items"]

def list_employers(text):
    url = f'https://api.hh.ru/employers'
    params = {
        'per_page': 100,
        'text': text,
        'area': '1',
        'page': '0',
    }
    data = get_request(url, params)
    return data

def list_vacancies(employer):
    url = f'https://api.hh.ru/vacancies?employer_id={employer}'
    params = {
         'per_page': 100,
         'text': 'Paython',
         'area': '1',
         'page': '0',
    }
    # data = get_request(url, params)
    vacancies = []

    for page in range(5):
        params["page"] = page
        data = get_request(url, params)
        # print(len(data))
        vacancies.extend(data)
    return vacancies


def add_employer(db_hh, text='сбер'):
    # db_hh = DBManager()
    # print(db_hh)
    """Добавить компанию"""
    # список компаний по введенному слову
    list_emps = list_employers(text)
    finish_employer = False
    if len(list_emps) == 1:
        # одна компания добавляем ее
        id = list_emps[0]['id']
        name = list_emps[0]['name']
    else:

        while not finish_employer:

            print("Найдено много компаний. Ведите ID компании которую надо добавить из списка")
            for ite in list_emps:
                print(f'({ ite["id"] }) - {ite["name"] } ')
            print(f'(0) - отмена')

            input_id_emp = str(input())
            # input_id_emp = '3529'
            if input_id_emp == '0':
                break
            else:
                id_emp = next((i for i, x in enumerate(list_emps) if x["id"] == input_id_emp), None)
                # print(id_emp)
                if id_emp == None:
                    print('Не найдена компания с таким id')
                else:
                    db_hh.db_add_employer(list_emps[id_emp]['id'], list_emps[id_emp]['name'])
                    add_vacancies(db_hh, list_emps[id_emp]['id'])
                    break


def add_vacancies(db_hh, employer):
    list_vac = list_vacancies(employer)
    for vac in list_vac:
        # salary=vac['salary_to']
        # print(vac)
        if vac['salary']:

            salary_from = vac['salary']['from']
            salary_to = vac['salary']['to']
            salary_currency = vac['salary']['currency']
            if salary_from == None:
                salary_from = 0
            if salary_to == None:
                    salary_to = 0

            if salary_from>0 and salary_to>0:
                salary = (salary_from + salary_to) / 2
            else:
                salary = salary_from + salary_to

        else:
            salary_from = None
            salary_to = None
            salary_currency = None
            salary = 0

        # print(salary_from)
        # print(salary_to)
        # print(f'agv {salary}')
        # print(vac['alternate_url'])

        db_hh.db_add_vacancies(vac['id'], employer,  vac['name'], vac['alternate_url']
                               ,vac['published_at'], vac['area']['name'], salary_from,
                               salary_to, salary_currency, salary)