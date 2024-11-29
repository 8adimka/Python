from flask import Flask, render_template, request, redirect, url_for
import json, os

app = Flask (__name__)

UPLOAD_FOLDER = '/home/v/Python/c3l2_flask_HTML_CSS/static/uploads'  # путь к папке для сохранения изображений
FILE_DB = '/home/v/Python/c3l2_flask_HTML_CSS/publications.json'  # Путь к JSON-файлу для сохранения данных
password_path = '/home/v/Python/c3l2_flask_HTML_CSS/password_base.json' # Путь к JSON-файлу для сохранения логинов и паролей

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Создаём папку для загрузок, если её нет
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

# Создаём файл базы данных, если он отсутствует
if not os.path.exists(FILE_DB):
    with open(FILE_DB, 'w', encoding='utf-8') as f:
        json.dump([], f)

@app.route('/')
def start_page ():
    return render_template('test2_start.html')

@app.route('/enter/')
def reg_page(): 
    return render_template('test2_reg.html')

# @app.route('/feed/', methods=['GET', 'POST'])
# def feed_page ():
#     return render_template('test2_feed.html')

@app.route('/feed/', methods=['GET', 'POST'])
def feed_page():
    # Загрузка публикации из базы данных
    with open(FILE_DB, 'r', encoding='utf-8') as f:
        publications = json.load(f)
    return render_template('test2_feed.html', UPLOAD_FOLDER=UPLOAD_FOLDER, publications=publications)

@app.route('/load/', methods=['GET', 'POST'])
def load_page():
    if request.method == 'POST':
        username = request.form.get('username', 'Аноним')  # Получить логин пользователя
        description = request.form.get('description', '')  # Получить описание
        file = request.files.get('file')  # Получить файл изображения

        if file:
            # Сохраняем файл
            filename = file.filename
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(filepath)

            # Сохраняем публикацию в базу данных
            with open(FILE_DB, 'r+', encoding='utf-8') as f:
                data = json.load(f)
                data.append({
                    'username': username,
                    'description': description,
                    'image': filename
                })
                f.seek(0)
                json.dump(data, f, ensure_ascii=False, indent=4)

        return redirect(url_for('feed_page'))
    return render_template('test2_load.html')

@app.route('/registr/', methods=['GET', 'POST'])
def registr_page ():
    username = request.form.get('username', '').lower()
    password = request.form.get('password', '')
    result = None
    
    if username and password:
        # Если файл существует, загрузить существующие данные
        if os.path.exists(password_path):
            with open(password_path, 'r', encoding='utf-8') as file:
                try:
                    data = json.load(file)  # Загрузить текущий словарь
                except json.JSONDecodeError:
                    data = {}  # Если файл поврежден или пуст, начать с пустого словаря
        else:
            data = {} # Если файла нет, создаем пустой словарь

        data[username] = password

        with open (password_path, 'w', encoding='utf-8') as file:
            json.dump(data, file)
            result = True

    return render_template('test2_registr.html', result=result)

@app.route('/login/', methods=['GET', 'POST'])
def user_password():
    username = request.form.get('username', '').lower()
    password = request.form.get('password', '')
    result = None

    if username and password:
        # Если файл существует, загрузить существующие данные
        if os.path.exists(password_path):
            with open(password_path, 'r', encoding='utf-8') as file:
                try:
                    data = json.load(file)  # Загрузить текущий словарь
                except json.JSONDecodeError:
                    result = None # Если файл поврежден или пуст
        if data[username] == password:
            result = True
        else:
            result = False
    return render_template('test2_login.html', result=result)

if __name__ == ('__main__'):
    # app.run (debug=True)
    app.run (host='0.0.0.0', port=5000)

