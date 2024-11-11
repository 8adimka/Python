from flask import Flask
import json
import os

file_path = os.path.join ('C:\\', 'Users', 'm8adi', 'Desktop', 'Python', 'Course3.Lecture1', 'candidates.json')

# Загрузка рабочих данных
def load_candidates(file_path):
    '''Загрузка данных из файла JSON'''
    try:
        with open (file_path) as file:
            return json.load (file)
    except:
        print(f'Ошибка загрузки данных')
        return None

candidates = load_candidates (file_path)

# Функции для работы с данными:
def get_by_pk(pk):
    '''вернет кандидата по pk'''
    for candidate in candidates:
        if candidate["pk"] == pk:
            return candidate
    return 'Кандидата с таким pk не найдено'

def get_by_skill(skill_name):
    '''вернет подходящих кандидатов по навыку'''
    result = ''
    for candidate in candidates:
        if skill_name.lower() in candidate["skills"].lower().strip().split(', '):
            result += f'Имя кандидата - {candidate["name"]}<br>Позиция кандидата - {candidate["position"]}<br>{candidate["skills"]}<br><br>'
    if result:
        return result
    return 'Кандидата с таким скилом не найдено'

# Запуск Flask       
app = Flask (__name__)

# Главная страница со списком кандидатов
@app.route('/')
def main_page ():
    result = ''
    if candidates:
        for candidate in candidates:
            result += f'Имя кандидата - {candidate["name"]}<br>Идентификационный номер кандидата кандидата - {candidate["pk"]}<br>{candidate["skills"]}<br><br>'
        return str (result)
    else:
        return 'Ошибка загрузки данных'

# Страница кандидата по pk   
@app.route('/<int:pk>/')
def candidate_page (pk):
    candidate = get_by_pk(pk)
    return f"""<img src='{candidate['picture']}'> 
<pre>
Имя кандидата - {candidate['name']}
Позиция кандидата - {candidate['position']}
{candidate['skills']}</pre>"""

# Поиск по навыку
@app.route('/skills/<skill>')
def skill_page (skill):
    result = get_by_skill(skill)
    return result

# if __main__ - Start
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
