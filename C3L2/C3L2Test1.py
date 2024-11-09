from flask import Flask, render_template, request
import os, random, json
app = Flask(__name__)

@app.route('/card')
def user_card():
    # Данные пользователя
    user_data = {
        "username": "alexy_001",
        "email": "alexy@skyeng.ru",
        "phone": "+1555223311"
    }
    # Передача данных в шаблон
    return render_template('user_card.html', **user_data)



@app.route('/city/')
@app.route('/city/<int:numb>')
def cites (numb = None):
    c_dict = {
        1: "Самара",
        2: "Краснодар",
        3: "Сочи",
        4: "Новосибирск",
        5: "Вышгород"
        }
    results = numb
    return render_template('city.html', c_dict = c_dict, results=results)



ws = [
    "платина", "стена", "халат", "блокнот", "косилка", 
    "автобус", "базар", "биосфера", "грелка"
]
@app.route('/search/')
def search():
    query = request.args.get('s', '') # Получаем именованный ('s') input из HTML-документа
    results = []

    if query: 
        results = [word for word in ws if query.lower() in word.lower()] # Приводим к нижнему регистру для нечувствительности к регистру

    return render_template('search.html', results=results if query else None)



@app.route('/form/')
def user_form():
    username = request.args.get('username', '')
    level = request.args.get('level', '')

    if username or level:
        with open (r'C:\Users\m8adi\Desktop\Python\C3L2\records.txt', 'a', encoding='utf-8') as file:
            file.write (f'username : {username}, level : {level}\n')
    
    return render_template('user_form.html')


DATA_BASE = {'v': 'Killer1911!', 'm8adimka': 'Killer1911!'}
@app.route('/pass/', methods=['GET', 'POST'])
def user_password():
    username = request.form.get('username', '').lower()
    password = request.form.get('password', '')

    if username in DATA_BASE and DATA_BASE[username] == password:
        results = username
    else:
        results = False

    return render_template('user_password.html', results=results)

# @app.route('/', methods=['GET', 'POST'])
# def user_password():
#     results = None
#     if request.method == 'POST':
#         username = request.form.get('username', '').lower()  # Получаем username из формы, приводим к нижнему регистру
#         password = request.form.get('password', '')  # Получаем password из формы

#         # Проверка данных в базе
#         if username in DATA_BASE and DATA_BASE[username] == password:
#             results = username  # Если данные корректны, сохраняем имя пользователя
#         else:
#             results = False  # Если данные неверны, указываем доступ запрещен

#     return render_template('user_password.html', results=results)



UPLOAD_FOLDER = r'C:\Users\m8adi\Desktop\Python\C3L2\uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Создаем папку uploads, если её нет
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

@app.route('/load/', methods=['GET', 'POST'])
def upload_file():
    message = ""
    if request.method == 'POST':
        if 'file' not in request.files:
            message = 'Файл не найден'
        else:
            file = request.files['file']
            if file.filename == '':
                message = 'Файл не выбран'
            else:
                filename_list = file.filename.split('.')
                filename = f'{random.randint(100000, 999999)}.{filename_list[-1]}'                
                file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
                file.save(file_path)
                message = f'Файл {filename} успешно загружен в {file_path}<br>'

                if filename_list[-1] in ['png', 'jpg', 'tiff', 'svg']:
                    message += 'и это картинка'
                elif filename_list[-1] in ['txt', 'doc', 'rtf']:
                    message += 'и это текст'
                else:
                    message += 'возможно это PDF или я не знаю такого формата'
    return render_template('file_load.html', message=message)


@app.route('/', methods=['GET', "POST"])
def upload_file2():
    message = ""
    if request.method == 'POST':
        if 'file' not in request.files:
            message = 'Файл не найден'
        else:
            file = request.files['file']
            if file.filename == '':
                message = 'Файл не выбран'
            else:
                UPLOAD_FOLDER = r'C:\Users\m8adi\Desktop\Python\C3L2'              
                folder_path = os.path.join(UPLOAD_FOLDER, request.form.get('folder', ''))
                if not os.path.exists(folder_path):
                    os.makedirs(folder_path)
                file_path = os.path.join(folder_path, file.filename)
                file.save(file_path)
                message = f'Файл {file.filename} успешно загружен в {file_path}<br>'
    return render_template('file_load2.html', message=message)


@app.route('/json/', methods=['GET', 'POST'])
def upload_file3():
    message = ""
    if request.method == 'POST':
        if 'file' not in request.files:
            message = 'Файл не найден'
        else:
            file = request.files['file']
            if file.filename == '':
                message = 'Файл не выбран'
            else:
                filename_list = file.filename.split('.')               
                if filename_list[-1].lower() == 'json':
                    data = json.load(file)
                    print(data)  # Выводим данные в консоль
                    message = f'JSON содержимое: {data}'
                else:
                    message = 'это не json'
    return render_template('file_load3.html', message=message)


if __name__ == "__main__":
    app.run()
