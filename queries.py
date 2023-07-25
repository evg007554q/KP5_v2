def select_only_employers():
    q_text = 'SELECT id, name	FROM employers'
    return q_text

def select_employers():
    q_text = '''SELECT employers.id, employers.name, count(vacancies.id)	
    FROM employers
        inner join vacancies
            on vacancies.employer_id = employers.id
    GROUP BY
    employers.id, employers.name
    '''
    return q_text

def select_all_vacancies():
    q_text = '''
    SELECT  employers.name,  vacancies.*	
        FROM employers
            inner join vacancies
                on vacancies.employer_id = employers.id
        
        '''
    return q_text


def select_top_vacancies():
    q_text = '''
        SELECT employers.name, vacancies.*	
        FROM employers
            inner join vacancies
                on vacancies.employer_id = employers.id
        order by salary desc
		limit 5
        '''
    return q_text


def select_vacancies_with_higher_salary():
    q_text = '''
        SELECT employers.name, vacancies.*	
        FROM employers
            inner join vacancies
                on vacancies.employer_id = employers.id
        where  vacancies.salary > (SELECT  AVG(vacancies.salary	) from   vacancies where salary > 0)       
        '''
    return q_text

def select_avg_salary():
    q_text = '''
        SELECT  AVG(vacancies.salary) from   vacancies where salary > 0       
        '''
    return q_text

def select_vacancies_with_keyword(keyword):
    q_text = f"""
        SELECT employers.name, vacancies.*	
        FROM employers
            inner join vacancies
                on vacancies.employer_id = employers.id
        where  vacancies.name like '%{keyword}%'    
        """
    return q_text