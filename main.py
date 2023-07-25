from configparser import ParsingError
import requests

import db_manager
from func import add_employer
from queries import select_employers


def main():
    db_hh = db_manager.DBManager()
    finish = False

    while not finish:
        employers = db_hh.get_companies_and_vacancies_count()
        if len(employers) == 0:
            #в базе нет компаний
            # command = '1'
            # уходим в меню работа с компаниями
            command = '1'
        else:
            command = input(
                             "1 - Список интересных компаний \n"
                             "2 - Список вакансий \n"
                             "3 - Средня ЗП по выбранным компаниям\n"
                             "0 - Выход \n"
                          )

        if command == '0':
            finish = True
            db_hh.conn.close()
            break

        elif command == '1':
            employers_menu(db_hh, employers)

        elif command == '2':
            vacancies_menu(db_hh)

        elif command == '3':
            print(db_hh.get_avg_salary())

def vacancies_menu(db_hh):
    """
    работа со списком вакансий
    """
    finish = False
    while not finish:
        print('')
        command = input(
               "1 - Список вакансий\n"
               "2 - 5 лучших вакансий\n"
               "3 - Вакансии с ЗП выше средней \n"
               "4 - Поиск по слову\n"
               "0 - Назад \n"
        )
        date_hh = None
        if command == '0':
            finish = True
            break
        elif command == '1':
            date_hh = db_hh.get_all_vacancies()

        elif command == '2':
            date_hh = db_hh.get_top_vacancies()

        elif command == '3':
            date_hh = db_hh.get_vacancies_with_higher_salary()

        elif command == '4':
            keyword = input("Введите ключевое слово для поиска\n")
            date_hh = db_hh.get_vacancies_with_keyword(keyword)

        if date_hh != None:
            # print(date_hh)
            for item in date_hh:
                print(item)
def employers_menu(db_hh, employers):
    """
    работа со списком компаний
    """
    finish = False
    while not finish:
        if len(employers) == 0:
            command = '1'
        else:
            print('Компании в базе:')
            for emp in employers:
                print(f'({emp[0]}) - {emp[1]} вакансий {emp[2]} ')
            finish = False
            print('')
            command = input(
                "1 - Добавить компанию\n"
                "2 - Удалить компанию\n"
                "0 - Назад \n"
            )
        #
        if command == '0':
            finish = True
            break
        elif command == '1':
            add_employers_menu(db_hh)
            employers = db_hh.get_companies_and_vacancies_count()
        elif command == '2':
            remove_employers_menu(db_hh)
            employers = db_hh.get_companies_and_vacancies_count()


def remove_employers_menu(db_hh):
    remove_employers_id = input("Введите id компании \n")
    # не будем искать и проверять есть ли такой контрагент этого не просят
    # удалим все записи по веденному ID
    db_hh.db_remove_employers(remove_employers_id)


def add_employers_menu(db_hh):
    keyword = input("Введите название компании \n")
    # keyword = 'sber'
    # print(db_hh)
    add_employer(db_hh, keyword)

if __name__ == "__main__":
    main()
    # employers_menu()

