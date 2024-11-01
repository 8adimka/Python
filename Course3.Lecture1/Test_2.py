from flask import Flask
import json
import os

app = Flask (__name__)

def load_from_json (file_path):
    with open (file_path) as file:
        return json.load(file)
    
file_path = os.path.join ('C:\\', 'Users', 'm8adi', 'Desktop', 'Python', 'Course3.Lecture1', 'num_list.json')
numb_list = load_from_json(file_path)
# numb_list = load_from_json(r'C:\Users\m8adi\Desktop\Python\Course3.Lecture1\num_list.json')

text = """<pre>
На крыльце сидел котейка
Мимо шел казах Андрейка
Будет завтра у Андрейки
из котейки тюбетейка
</pre>"""

@app.route('/')
def main_page():
    return text


@app.route ('/find/<word>')
def find_page (word):
    if word in text:
        return 'Да, есть такое слово'
    else:
        return 'Не, такого слова нет'


@app.route('/first/')
def first_page ():
    return str(numb_list[0])
@app.route('/last/')
def last_page ():
    return str(numb_list[-1])
@app.route('/sum/')
def sum_page ():
    return str(sum(numb_list))


city_dict = {1: "Самара", 2: "Краснодар", 3: "Сочи", 4: "Новосибирск", 5: "Вышгород"}
@app.route ('/city/<int:num>/')
def city_page (num):
    return city_dict[num]


@app.route ('/kbytes/<int:mbytes>/')
def kb_page (mbytes):
    return f'<pre> В {mbytes} мб будет - {round(mbytes*1024)} килобайт </pre>'
@app.route ('/bytes/<int:mbytes>/')
def b_page (mbytes):
    return f'В {mbytes} мб будет - {round(mbytes*1024*1024)} байт'


records = []
@app.route ('/add/<word>/')
def add_page (word):
    records.append(word)
    return f"Слово {word} - добавлено в список"
@app.route ('/show/')
def show_page ():
    return ', '.join(records)

@app.route('/meal/')
@app.route('/meal/<first>/')
@app.route('/meal/<first>/<second>/')
@app.route('/meal/<first>/<second>/<third>/')
def lunch_page(first=None, second=None, third=None):
    if first:
        result = (f'На первое: {first}')
        if second:
            result += (f'<br>На второе: {second}')
            if third:
                result += (f'<br>На третье: {third}')
    else:
        return (f'На ланч ничего!')
    return result




if __name__ == '__main__':
    app.run()
