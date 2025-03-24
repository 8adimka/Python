
from typing import Optional

class Employer:
    def __init__(self, id: int, name: str, url: str, open_vacancies: int):
        self.id = id
        self.name = name
        self.url = url
        self.open_vacancies = open_vacancies

    def __repr__(self):
        return f"Employer(id={self.id}, name='{self.name}', url='{self.url}', open_vacancies={self.open_vacancies})"
    
class Vacancy:
    def __init__(self, id: int, employer_id: int, name: str, salary_from: Optional[int], 
                 salary_to: Optional[int], salary_currency: Optional[str], url: str):
        self.id = id
        self.employer_id = employer_id
        self.name = name
        self.salary_from = salary_from
        self.salary_to = salary_to
        self.salary_currency = salary_currency
        self.url = url

    def __repr__(self):
        return (f"Vacancy(id={self.id}, employer_id={self.employer_id}, name='{self.name}', "
                f"salary_from={self.salary_from}, salary_to={self.salary_to}, "
                f"salary_currency='{self.salary_currency}', url='{self.url}')")

    @property
    def salary_avg(self) -> Optional[float]:
        """Рассчитывает среднюю зарплату вакансии"""
        if self.salary_from and self.salary_to:
            return (self.salary_from + self.salary_to) / 2
        elif self.salary_from:
            return self.salary_from
        elif self.salary_to:
            return self.salary_to
        return None