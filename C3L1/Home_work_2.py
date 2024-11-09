from flask import Flask, jsonify
import json
import os

file_path = os.path.join ('C:\\', 'Users', 'm8adi', 'Desktop', 'Python', 'Course3.Lecture1', 'candidates.json')

app = Flask(__name__)

def load_candidates():
    '''Загрузка данных из файла JSON'''
    with open(file_path, "r", encoding="utf-8") as file:
        return json.load(file)

# Функции для работы с данными
def get_by_pk(pk):
    '''вернет кандидата по pk'''
    candidates = load_candidates()
    for candidate in candidates:
        if candidate["pk"] == pk:
            return candidate
    return None

def get_by_skill(skill_name):
    '''вернет подходящих кандидатов по навыку'''
    candidates = load_candidates()
    return [
        candidate for candidate in candidates
        if skill_name.lower() in candidate["skills"].lower()
    ]

# Главная страница со списком кандидатов
@app.route('/')
def main_page():
    candidates = load_candidates()
    result = "<pre>"
    for candidate in candidates:
        result += f"Имя кандидата - {candidate['name']}\n"
        result += f"Позиция кандидата - {candidate['position']}\n"
        result += f"Навыки через запятую - {candidate['skills']}\n\n"
    result += "</pre>"
    return result

# Страница кандидата по pk
@app.route('/candidates/<int:pk>')
def candidate_page(pk):
    candidate = get_by_pk(pk)
    if candidate:
        result = f"<img src='{candidate['picture']}'><pre>\n"
        result += f"Имя кандидата - {candidate['name']}\n"
        result += f"Позиция кандидата - {candidate['position']}\n"
        result += f"Навыки через запятую - {candidate['skills']}\n</pre>"
        return result
    else:
        return "Кандидат не найден", 404

# Поиск по навыку
@app.route('/skills/<skill>')
def skills_page(skill):
    candidates = get_by_skill(skill)
    if candidates:
        result = "<pre>"
        for candidate in candidates:
            result += f"Имя кандидата - {candidate['name']}\n"
            result += f"Позиция кандидата - {candidate['position']}\n"
            result += f"Навыки через запятую - {candidate['skills']}\n\n"
        result += "</pre>"
        return result
    else:
        return f"Нет кандидатов со скиллом '{skill}'", 404

# Запуск приложения
if __name__ == '__main__':
    app.run(debug=True)

