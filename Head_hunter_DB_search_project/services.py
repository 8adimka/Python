from typing import Dict, List
from api_client import HeadHunterAPI
from db_manager import DBManager


class DataCollector:
    """Сервис для сбора данных о работодателях и вакансиях"""
    
    def __init__(self, api: HeadHunterAPI, db_manager: DBManager):
        self.api = api
        self.db_manager = db_manager
    
    def collect_data(self, companies: List[Dict]):
        """Собирает данные о компаниях и их вакансиях и сохраняет в базу данных"""
        print("Начало сбора данных...")
        
        # Создаем таблицы, если они еще не существуют
        self.db_manager.create_tables()
        
        for company in companies:
            print(f"Обработка компании: {company['name']}...")
            
            # Получаем информацию о работодателе
            employer = self.api.get_employer(company['id'])
            if employer:
                self.db_manager.insert_employer(employer)
                
                # Получаем вакансии работодателя
                vacancies = self.api.get_vacancies(company['id'])
                for vacancy in vacancies:
                    self.db_manager.insert_vacancy(vacancy)
                
                print(f"Добавлено {len(vacancies)} вакансий для {company['name']}")
            else:
                print(f"Не удалось получить данные для компании {company['name']}")
        
        print("Сбор данных завершен!")
        