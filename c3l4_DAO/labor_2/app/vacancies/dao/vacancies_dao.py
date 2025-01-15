import json

class VacanciesDAO:

    def __init__(self, path):
        self.path = path

    def load_data(self):
        with open(self.path, "r", encoding="utf-8") as file:
            data = json.load(file)
        return data

    def get_all(self):
        vacancies = self.load_data()
        return vacancies

    def get_by_pk(self, pk):
        vacancies = self.load_data()
        for vacancy in vacancies:
            if vacancy["pk"] == pk:
                return vacancy
            