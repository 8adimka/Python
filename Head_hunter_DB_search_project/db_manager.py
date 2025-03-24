from typing import Dict, List, Tuple, Optional
import psycopg2
from psycopg2.extras import DictCursor
from psycopg2 import sql
from dto.models import Employer, Vacancy

class DBManager:
    """Класс для работы с базой данных PostgreSQL"""
    
    def __init__(self, config: Dict):
        self.config = config
        self.conn = None
        self._connect()
    
    def _connect(self):
        """Устанавливает соединение с базой данных"""
        try:
            self.conn = psycopg2.connect(**self.config)
            self.conn.autocommit = True
            print("Соединение с PostgreSQL установлено")
        except psycopg2.Error as e:
            print(f"Ошибка подключения к базе данных: {e}")
            raise

    def __enter__(self):
        if self.conn is None or self.conn.closed:
            self._connect()
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()
    
    def close(self):
        """Закрывает соединение с базой данных"""
        if self.conn and not self.conn.closed:
            self.conn.close()
            self.conn = None
            print("Соединение с PostgreSQL закрыто")

    def create_tables(self):
        """Создает таблицы в базе данных"""
        if self.conn is None or self.conn.closed:
            self._connect()
        
        try:
            with self.conn.cursor() as cursor:
                cursor.execute("""
                    CREATE TABLE IF NOT EXISTS employers (
                        id INTEGER PRIMARY KEY,
                        name VARCHAR(255) NOT NULL,
                        url VARCHAR(255),
                        open_vacancies INTEGER
                    )
                """)
                
                cursor.execute("""
                    CREATE TABLE IF NOT EXISTS vacancies (
                        id INTEGER PRIMARY KEY,
                        employer_id INTEGER REFERENCES employers(id),
                        name VARCHAR(255) NOT NULL,
                        salary_from INTEGER,
                        salary_to INTEGER,
                        salary_currency VARCHAR(10),
                        url VARCHAR(255)
                    )
                """)
                print("Таблицы успешно созданы")
        except psycopg2.Error as e:
            print(f"Ошибка при создании таблиц: {e}")
            raise
    
    def insert_employer(self, employer: Employer):
        """Добавляет работодателя в базу данных"""
        if self.conn is None or self.conn.closed:
            self._connect()
            
        try:
            with self.conn.cursor() as cursor:
                cursor.execute("""
                    INSERT INTO employers (id, name, url, open_vacancies)
                    VALUES (%s, %s, %s, %s)
                    ON CONFLICT (id) DO UPDATE SET
                        name = EXCLUDED.name,
                        url = EXCLUDED.url,
                        open_vacancies = EXCLUDED.open_vacancies
                """, (employer.id, employer.name, employer.url, employer.open_vacancies))
        except psycopg2.Error as e:
            print(f"Ошибка при добавлении работодателя: {e}")
            raise
    
    def insert_vacancy(self, vacancy: Vacancy):
        """Добавляет вакансию в базу данных"""
        if self.conn is None or self.conn.closed:
            self._connect()
            
        try:
            with self.conn.cursor() as cursor:
                cursor.execute("""
                    INSERT INTO vacancies (id, employer_id, name, salary_from, salary_to, salary_currency, url)
                    VALUES (%s, %s, %s, %s, %s, %s, %s)
                    ON CONFLICT (id) DO UPDATE SET
                        employer_id = EXCLUDED.employer_id,
                        name = EXCLUDED.name,
                        salary_from = EXCLUDED.salary_from,
                        salary_to = EXCLUDED.salary_to,
                        salary_currency = EXCLUDED.salary_currency,
                        url = EXCLUDED.url
                """, (vacancy.id, vacancy.employer_id, vacancy.name, 
                     vacancy.salary_from, vacancy.salary_to, vacancy.salary_currency, vacancy.url))
        except psycopg2.Error as e:
            print(f"Ошибка при добавлении вакансии: {e}")
            raise
    
    def get_companies_and_vacancies_count(self) -> List[Tuple[str, int]]:
        """Получает список всех компаний и количество вакансий у каждой компании"""
        if self.conn is None or self.conn.closed:
            self._connect()
            
        try:
            with self.conn.cursor(cursor_factory=DictCursor) as cursor:
                cursor.execute("""
                    SELECT e.name, COUNT(v.id) as vacancies_count
                    FROM employers e
                    LEFT JOIN vacancies v ON e.id = v.employer_id
                    GROUP BY e.id, e.name
                    ORDER BY vacancies_count DESC
                """)
                return cursor.fetchall()
        except psycopg2.Error as e:
            print(f"Ошибка при получении данных: {e}")
            raise
    
    def get_all_vacancies(self) -> List[Dict]:
        """Получает список всех вакансий с указанием названия компании, названия вакансии и зарплаты и ссылки на вакансию"""
        if self.conn is None or self.conn.closed:
            self._connect()
            
        try:
            with self.conn.cursor(cursor_factory=DictCursor) as cursor:
                cursor.execute("""
                    SELECT e.name as company_name, v.name as vacancy_name, 
                           v.salary_from, v.salary_to, v.salary_currency, v.url
                    FROM vacancies v
                    JOIN employers e ON v.employer_id = e.id
                    ORDER BY e.name, v.name
                """)
                return cursor.fetchall()
        except psycopg2.Error as e:
            print(f"Ошибка при получении вакансий: {e}")
            raise
    
    def get_avg_salary(self) -> float:
        """Получает среднюю зарплату по вакансиям"""
        if self.conn is None or self.conn.closed:
            self._connect()
            
        try:
            with self.conn.cursor() as cursor:
                cursor.execute("""
                    SELECT AVG((COALESCE(salary_from, 0) + COALESCE(salary_to, 0)) / 2) as avg_salary
                    FROM vacancies
                    WHERE salary_from IS NOT NULL OR salary_to IS NOT NULL
                """)
                result = cursor.fetchone()
                return result[0] if result[0] else 0.0
        except psycopg2.Error as e:
            print(f"Ошибка при расчете средней зарплаты: {e}")
            raise
    
    def get_vacancies_with_higher_salary(self) -> List[Dict]:
        """Получает список всех вакансий, у которых зарплата выше средней по всем вакансиям"""
        avg_salary = self.get_avg_salary()
        
        if self.conn is None or self.conn.closed:
            self._connect()
            
        try:
            with self.conn.cursor(cursor_factory=DictCursor) as cursor:
                cursor.execute("""
                    SELECT e.name as company_name, v.name as vacancy_name, 
                           v.salary_from, v.salary_to, v.salary_currency, v.url
                    FROM vacancies v
                    JOIN employers e ON v.employer_id = e.id
                    WHERE (COALESCE(v.salary_from, 0) + COALESCE(v.salary_to, 0)) / 2 > %s
                    ORDER BY (COALESCE(v.salary_from, 0) + COALESCE(v.salary_to, 0)) / 2 DESC
                """, (avg_salary,))
                return cursor.fetchall()
        except psycopg2.Error as e:
            print(f"Ошибка при получении вакансий: {e}")
            raise
    
    def get_vacancies_with_keyword(self, keyword: str) -> List[Dict]:
        """Получает список всех вакансий, в названии которых содержатся переданные в метод слова"""
        if self.conn is None or self.conn.closed:
            self._connect()
            
        try:
            with self.conn.cursor(cursor_factory=DictCursor) as cursor:
                cursor.execute("""
                    SELECT e.name as company_name, v.name as vacancy_name, 
                           v.salary_from, v.salary_to, v.salary_currency, v.url
                    FROM vacancies v
                    JOIN employers e ON v.employer_id = e.id
                    WHERE LOWER(v.name) LIKE %s
                    ORDER BY e.name, v.name
                """, (f"%{keyword.lower()}%",))
                return cursor.fetchall()
        except psycopg2.Error as e:
            print(f"Ошибка при поиске вакансий: {e}")
            raise
