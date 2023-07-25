import psycopg2
from psycopg2 import DatabaseError
import os

from queries import select_employers, select_vacancies_with_keyword, select_vacancies_with_higher_salary, \
    select_top_vacancies, select_all_vacancies, select_avg_salary


psw= os.getenv('PAS_POSTGSQL')

class DBManager:
    def __init__(self):
        self.conn = psycopg2.connect(
            dbname='kp5'
            ,user='postgres'
            ,host='localhost'
            ,password=psw)
        self.conn.autocommit = True

    def qw(self, queries_text):
        try:
            with self.conn.cursor() as cur:
                cur.execute(queries_text)
                return cur.fetchall()
        except DatabaseError as e:
            print(e)
            raise DatabaseError

    def db_add_employer(self, id, name):
        self.conn.autocommit = True
        with self.conn.cursor() as cur:
              cur.execute(f"INSERT INTO public.employers(id, name) select '{id}', '{name}' where not exists (select id from employers where id='{id}')")
              # cur.execute("INSERT INTO employers(id, name) values (%s, %s) ",(1311,'11111'))
              # cur.close()
        # self.conn.close()

        return None

    def db_remove_employers(self, employer_id):
        with self.conn.cursor() as cur:
            cur.execute(f"DELETE FROM public.employers  where  id = '{employer_id}'")
        with self.conn.cursor() as cur:
            cur.execute(f"DELETE FROM public.vacancies  where  employer_id = '{employer_id}'")

    def db_add_vacancies(self, id, employer_id, name, alternate_url,
                        published_at, area, salary_from,
                        salary_to, salary_currency, salary):
        # self.conn.autocommit = True
        with self.conn.cursor() as cur:
              cur.execute("INSERT INTO "
                          "vacancies(id, employer_id, name, alternate_url, "
                          "published_at, area, salary_from, "
                          "salary_to, salary_currency, salary) values "
                          "(%s, %s, %s, %s  "
                          ",%s, %s, %s  "
                          ",%s, %s, %s) "
                          ,
                          (id, employer_id, name, alternate_url,
                          published_at, area, salary_from,
                          salary_to, salary_currency, salary))
              # cur.close()
        # self.conn.close()

        return None

    def get_companies_and_vacancies_count(self):
        # - get_companies_and_vacancies_count(): получает список всех компаний и количество вакансий у каждой компании.
        return self.qw(select_employers())

    def get_all_vacancies(self):
        # - get_all_vacancies(): получает список всех вакансий с указанием названия компании, названия вакансии и зарплаты и ссылки на вакансию.
        return self.qw(select_all_vacancies())

    def get_top_vacancies(self):
        return self.qw(select_top_vacancies())

    def get_vacancies_with_higher_salary(self):
        # - get_vacancies_with_higher_salary(): получает список всех вакансий, у которых зарплата выше средней по всем вакансиям.
        return self.qw(select_vacancies_with_higher_salary())

    def get_vacancies_with_keyword(self,keyword):
        # - get_vacancies_with_keyword(): получает список всех вакансий, в названии которых содержатся переданные в метод слова, например “python”.
        return self.qw(select_vacancies_with_keyword(keyword))

    def get_avg_salary(self):
        # - get_avg_salary(): получает среднюю зарплату по вакансиям.
        return self.qw(select_avg_salary())

