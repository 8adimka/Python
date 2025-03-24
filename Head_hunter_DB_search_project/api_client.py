import requests
from typing import List, Dict, Optional
import time
from dto.models import Employer, Vacancy

class HeadHunterAPI:
    """Класс для работы с API HeadHunter"""
    
    BASE_URL = 'https://api.hh.ru/'
    
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Accept': 'application/json',
            'HH-User-Agent': 'MyVacancyApp/1.0 (contact@myvacancyapp.com)',
            'Accept-Language': 'en-US,en;q=0.9',
            'Accept-Encoding': 'gzip, deflate, br'
        })
    
    def get_employer(self, employer_id: int) -> Optional[Employer]:
        url = f"{self.BASE_URL}employers/{employer_id}"
        try:
            response = self.session.get(url)
            response.raise_for_status()
            data = response.json()
            
            # Добавьте проверку данных
            required_fields = ['id', 'name', 'alternate_url', 'open_vacancies']
            if not all(field in data for field in required_fields):
                print(f"Отсутствуют необходимые поля в ответе: {data}")
                return None
                
            return Employer(
                id=int(data['id']),
                name=data['name'],
                url=data['alternate_url'],
                open_vacancies=data['open_vacancies']
            )
        except Exception as e:
            print(f"Ошибка при получении данных работодателя: {e}")
            return None
            
        except requests.exceptions.RequestException as e:
            print(f"Ошибка при запросе работодателя {employer_id}: {str(e)}")
            if hasattr(e, 'response') and e.response is not None:
                print(f"Статус код: {e.response.status_code}")
                try:
                    print(f"Ответ сервера: {e.response.json()}")
                except:
                    print(f"Ответ сервера: {e.response.text[:200]}...")
            return None
    
    def get_vacancies(self, employer_id: int) -> List[Dict]:
        """Получает и фильтрует вакансии по критериям:
        - Должность содержит 'python' (без учета регистра)
        - Зарплата от min_salary*
        """
        url = f"{self.BASE_URL}vacancies"
        params = {
            'employer_id': employer_id,
            'per_page': 100,  # Максимальное количество на странице
            'page': 0,
            'text': 'python',  # Фильтр по ключевому слову
            'only_with_salary': True  # Только вакансии с зарплатой
        }
        filtered_vacancies = []
        min_salary = 80000  # Минимальная зарплата в рублях
        
        while True:
            try:
                time.sleep(0.5)  # Задержка между запросами
                response = self.session.get(url, params=params, timeout=15)
                response.raise_for_status()
                data = response.json()
                
                for vacancy in data['items']:
                    if self._is_vacancy_valid(vacancy, min_salary):
                        filtered_vacancies.append(vacancy)
                
                if params['page'] >= data['pages'] - 1:
                    break
                params['page'] += 1
                
            except requests.exceptions.RequestException as e:
                print(f"Ошибка при запросе вакансий: {str(e)}")
                break
        
        return filtered_vacancies

    def _is_vacancy_valid(self, vacancy: Dict, min_salary_rub: int) -> bool:
        """Проверяет вакансию на соответствие критериям"""
        # Проверка ключевого слова в названии
        if 'python' not in vacancy['name'].lower():
            return False
        
        # Проверка зарплаты
        salary = vacancy.get('salary')
        if not salary:
            return False
        
        # Конвертация в рубли, если валюта другая
        salary_from = salary.get('from')
        salary_to = salary.get('to')
        currency = salary.get('currency', '').upper()
        
        # Примерные курсы валют (можно обновлять)
        exchange_rates = {
            'RUR': 1,    # Рубли
            'RUB': 1,    # Рубли
            'USD': 90,   # Примерный курс доллара
            'EUR': 100,  # Примерный курс евро
            'KZT': 0.2   # Примерный курс тенге
        }
        
        rate = exchange_rates.get(currency, 1)
        
        # Проверяем, что хотя бы одна часть зарплаты (from или to) >= min_salary_rub
        if salary_from and (salary_from * rate) >= min_salary_rub:
            return True
        if salary_to and (salary_to * rate) >= min_salary_rub:
            return True
        
        return False
    
    def _parse_vacancies(self, items: List[Dict]) -> List[Vacancy]:
        """Парсит список вакансий из API в список объектов Vacancy"""
        vacancies = []
        
        for item in items:
            try:
                salary = item.get('salary', {})
                
                vacancies.append(Vacancy(
                    id=int(item['id']),
                    employer_id=int(item['employer']['id']),
                    name=item['name'],
                    salary_from=salary.get('from'),
                    salary_to=salary.get('to'),
                    salary_currency=salary.get('currency'),
                    url=item['alternate_url']
                ))
            except (KeyError, ValueError) as e:
                print(f"Ошибка парсинга вакансии {item.get('id', 'unknown')}: {str(e)}")
                continue
        
        return vacancies
    