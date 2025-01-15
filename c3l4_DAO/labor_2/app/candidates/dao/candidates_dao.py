import json

class CandidateDAO:

    def __init__(self, path):
        """ При создании экземпляра DAO нужно указать путь к файлу с данными"""
        self.path = path

    def load_data(self):
        """ Загружает данные из файла и возвращает обычный list"""
        with open(self.path, "r", encoding="utf-8") as file:
            data = json.load(file)
        return data

    def get_all(self):
        """ Возвращает список со всеми данными"""
        candidates = self.load_data()
        return candidates

    def get_by_pk(self, pk):
        """ Возвращает одного кандидата по его номеру"""
        candidates = self.load_data()
        for candidate in candidates:
            if candidate["pk"] == pk:
                return candidate
            