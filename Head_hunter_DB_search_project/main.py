import time
from typing import List, Dict

from db_manager import DBManager
from api_client import HeadHunterAPI
from config import DATABASE_CONFIG, COMPANIES
from dto.models import Employer, Vacancy

def check_db_connection() -> bool:
    """Проверяет соединение с базой данных"""
    try:
        with DBManager(DATABASE_CONFIG) as db:
            return True
    except Exception as e:
        print(f"❌ Ошибка подключения к PostgreSQL: {e}")
        return False

def collect_and_analyze_data():
    """Основная функция сбора и анализа данных"""
    api = HeadHunterAPI()
    
    try:
        with DBManager(DATABASE_CONFIG) as db:
            print("\n🔄 Начало сбора данных...")
            db.create_tables()
            
            # Сбор данных по компаниям
            for company in COMPANIES:
                process_company(api, db, company)
                time.sleep(0.5)  # Задержка между запросами
            
            print("\n🎉 Сбор данных завершен!")
            show_statistics(db)
            
    except Exception as e:
        print(f"\n❌ Критическая ошибка: {e}")
        raise

def process_company(api: HeadHunterAPI, db: DBManager, company: Dict):
    """Обрабатывает данные одной компании"""
    print(f"\n🔍 Обработка компании: {company['name']}...")
    
    # Получаем объект Employer
    employer = api.get_employer(company['id'])
    if not employer:
        print(f"⚠️ Не удалось получить данные для {company['name']}")
        return
    
    # Сохраняем работодателя
    try:
        db.insert_employer(employer)
        print(f"✅ Работодатель {employer.name} успешно сохранён")
        
        # Получаем сырые данные вакансий
        vacancies_raw_data = api.get_vacancies(company['id'])
        vacancies_count = 0

        for vacancy_data in vacancies_raw_data:
            try:
                # Безопасное извлечение данных о зарплате
                salary_data = vacancy_data.get('salary') or {}
                
                vacancy = Vacancy(
                    id=int(vacancy_data['id']),
                    employer_id=int(vacancy_data['employer']['id']),
                    name=vacancy_data['name'],
                    salary_from=salary_data.get('from'),
                    salary_to=salary_data.get('to'),
                    salary_currency=salary_data.get('currency'),
                    url=vacancy_data['alternate_url']
                )
                db.insert_vacancy(vacancy)
                vacancies_count += 1
            except Exception as e:
                print(f"⚠️ Ошибка при обработке вакансии {vacancy_data.get('id', 'unknown')}: {str(e)}")
                continue
        
        print(f"✅ Добавлено {vacancies_count} вакансий для {company['name']}")
        
    except Exception as e:
        print(f"⚠️ Критическая ошибка при обработке компании {company['name']}: {e}")

def show_statistics(db: DBManager):
    """Выводит статистику по собранным данным"""
    print("\n📊 Статистика:")
    
    # Компании и количество вакансий
    print("\nКомпании и количество вакансий:")
    try:
        companies_stats = db.get_companies_and_vacancies_count()
        for company in companies_stats:
            print(f"- {company['name']}: {company['vacancies_count']}")
    except Exception as e:
        print(f"⚠️ Ошибка при получении статистики по компаниям: {e}")
    
    # Средняя зарплата
    try:
        avg_salary = db.get_avg_salary()
        print(f"\nСредняя зарплата: {avg_salary:.2f} RUB")
    except Exception as e:
        print(f"⚠️ Ошибка при расчете средней зарплаты: {e}")
    
    # Вакансии с зарплатой выше средней
    print("\n🔝 Вакансии с зарплатой выше средней:")
    try:
        high_salary_vacancies = db.get_vacancies_with_higher_salary()
        for vacancy in high_salary_vacancies:
            salary_from = vacancy['salary_from'] or "не указана"
            salary_to = vacancy['salary_to'] or "не указана"
            currency = vacancy['salary_currency'] or ""
            print(f"- {vacancy['company_name']}: {vacancy['vacancy_name']} (от {salary_from} до {salary_to} {currency})")
    except Exception as e:
        print(f"⚠️ Ошибка при получении вакансий с высокой зарплатой: {e}")
    
    # Поиск по ключевому слову
    keyword = "python"
    print(f"\n🔎 Вакансии по ключевому слову '{keyword}':")
    try:
        keyword_vacancies = db.get_vacancies_with_keyword(keyword)
        for vacancy in keyword_vacancies:
            print(f"- {vacancy['company_name']}: {vacancy['vacancy_name']}")
    except Exception as e:
        print(f"⚠️ Ошибка при поиске вакансий по ключевому слову: {e}")

if __name__ == "__main__":
    if not check_db_connection():
        exit(1)
    
    collect_and_analyze_data()
    