from flask import Flask
import json
import os

records = '''
1 Литвинова Анисья +7(927)636-82-95
2 Берестов Гордей +7(906)547-02-30
3 Соболев Самсон +7(910)318-27-21
4 Преображенский Вышеслав +7(972)271-19-88
5 Нектов Христофор +7(979)678-94-65
'''
file_path = os.path.join ('C:\\', 'Users', 'm8adi', 'Desktop', 'Python', 'Course3.Lecture1', 'records.json')

with open (file_path, 'w', encoding='utf-8') as file:
    json.dump(records, file)

def load_json (file_path):
    with open (file_path, 'r', encoding='utf-8') as file:
        record = json.load(file)
    return record

record_file = load_json (file_path)
record_list = record_file.strip().split('\n')
new_list = []
for record in record_list:
    record_dict = {}
    record_dict ['id'] = int(record[0])
    v = record[2:].strip().split(' ')
    record_dict ['name'] = f'{v[0]} {v[1]}'
    record_dict ['phone'] = v[2]
    new_list.append(record_dict)

app = Flask (__name__)

@app.route ('/')
def main_page ():
    result = ''
    for i in new_list:
        result += f"<br>id - {i['id']}, имя - {i['name']}"
    return f'{result}'

@app.route ('/<int:user_id>/')
def user_page (user_id):
    for i in new_list:
        if i['id']==user_id:
            return f'<pre>Имя пользователя - {i["name"]}\nНомер телефона - {i["phone"]}</pre>'
    return f'Пользователь с таким ID не найден'


if __name__ == '__main__':
    app.run()
