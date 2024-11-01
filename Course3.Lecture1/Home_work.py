import json
import os
from flask import Flask

# Принимаем данные
# candidates.json
file_json = [
  {
    "pk": 1,
    "name": "Adela Hendricks",
    "picture": "https://picsum.photos/200",
    "position": "Go разработчик",
    "gender": "female",
    "age": 40,
    "skills": "go, python"
  },
  {
    "pk": 2,
    "name": "Sheri Torres",
    "picture": "https://picsum.photos/200",
    "position": "Delphi developer",
    "gender": "female",
    "age": 26,
    "skills": "Delphi, pascal, fortran, basic"
  },
  {
    "pk": 3,
    "name": "Burt Stein",
    "picture": "https://picsum.photos/200",
    "position": "Team lead",
    "gender": "male",
    "age": 33,
    "skills": "делегирование, пользоваться календарем, обсуждать важные вопросы"
  },
  {
    "pk": 4,
    "name": "Bauer Adkins",
    "picture": "https://picsum.photos/200",
    "position": "CTO",
    "gender": "male",
    "age": 37,
    "skills": "very important face"
  },
  {
    "pk": 5,
    "name": "Day Holloway",
    "picture": "https://picsum.photos/200",
    "position": "HR manager",
    "gender": "male",
    "age": 35,
    "skills": "LinkedIn, telegram, spam, spam, spam"
  },
  {
    "pk": 6,
    "name": "Austin Cochran",
    "picture": "https://picsum.photos/200",
    "position": "python-develop",
    "gender": "male",
    "age": 26,
    "skills": "python, html"
  },
  {
    "pk": 7,
    "name": "Sheree Love",
    "picture": "https://picsum.photos/200",
    "position": "Django developer",
    "gender": "female",
    "age": 33,
    "skills": "Python, Django, flask"
  }
]

file_path = os.path.join ('C:\\', 'Users', 'm8adi', 'Desktop', 'Python', 'Course3.Lecture1', 'candidates.json')
with open (file_path, 'w') as file:
    json.dump (file_json, file)

def load_candidates():
    '''загрузит данные из файла'''
    with open (file_path) as file:
        return json.load(file)
    
def get_all():
    '''покажет всех кандидатов'''
    candidates = load_candidates()
    result = ("<pre>\n")
    for candidate in candidates:
        result += (f'Имя кандидата - {candidate["name"]}\nПозиция кандидата - {candidate["pk"]}\nНавыки: {candidate["skills"].title()}\n')
    result += "</pre>\n"
    return result

def get_by_pk(pk):
    '''вернет кандидата по pk'''
    candidates = load_candidates()
    for candidate in candidates:
        if candidate["pk"] == pk:
            return candidate

def get_by_skill(skill_name):
    '''вернет подходящих кандидатов по навыку'''
    valid_candidates=[]
    candidates = load_candidates()
    for candidate in candidates:
        if skill_name.lower() in candidate["skills"].lower():
            valid_candidates.append (candidate)
    return valid_candidates

app = Flask (__name__)

@app.route('/')
def main_page ():
    return get_all()

@app.route('/candidates/<int:pk>/')
def candidates_page (pk):
    candidate = get_by_pk(pk)
    if candidate:
        result = f"<img src='{candidate['picture']}'>\n\n<pre>\nИмя кандидата - {candidate['name']}\nПозиция кандидата - {candidate['position']}\n{candidate['skills']}"
        return result
    else:
        return "Кандидат не найден", 404

@app.route('/skills/<skill>/')
def skills_page(skill):
    candidates = get_by_skill(skill)
    if candidates:
        result = "<pre>"
        for candidate in candidates:
            result += f"Имя кандидата - {candidate['name']}\n"
            result += f"Позиция кандидата - {candidate['position']}\n"
            result += f"{candidate['skills']}\n\n"
        result += "</pre>"
        return result
    else:
        return f"Нет кандидатов со скиллом '{skill}'", 404

if __name__ == ('__main__'):
    app.run()




