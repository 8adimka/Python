from flask import Flask, render_template, request, redirect, url_for
import os, sqlite3

# Глобальная переменная для хранения user_id
current_user_id = None

app = Flask (__name__)

UPLOAD_FOLDER = '/home/v/Python/lesson16_flask_SQLAlchemy/static/uploads'  # путь к папке для сохранения изображений
PASSWORD_DB = '/home/v/Python/lesson16_flask_SQLAlchemy/my_book_SQL.db'

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

with sqlite3.connect (PASSWORD_DB) as con:
    cur = con.cursor()
    query = """CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name VARCHAR (100),
    password VARCHAR (250));

    CREATE TABLE IF NOT EXISTS posts (
    user_id INTEGER PRIMARY KEY,
    description TEXT,
    image VARCHAR (350),
    FOREIGN KEY (user_id) REFERENCES users(id));
    """
    cur.executescript (query)

# Создаём папку для загрузок, если её нет
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

@app.route('/')
def start_page ():
    return render_template('test2_start.html')

@app.route('/enter/')
def reg_page(): 
    return render_template('test2_reg.html')

@app.route('/registr/', methods=['GET', 'POST'])
def registr_page ():
    global current_user_id  # Используем глобальную переменную

    username = request.form.get('username', '').lower()
    user_password = request.form.get('password', '')
    result = None

    if username and user_password:
        with sqlite3.connect (PASSWORD_DB) as con:
            cur = con.cursor()
            cur.execute("INSERT INTO users (name, password) VALUES (?, ?)", (username, user_password))
            cur.execute("""SELECT users.name, users.id FROM users""")
            user_name_list = cur.fetchall()
            for user in user_name_list:
                if user[0] == username:
                    current_user_id = user[1]

            result = True

    return render_template('test2_registr.html', result=result)

@app.route('/login/', methods=['GET', 'POST'])
def user_password():
    username = request.form.get('username', '').lower()
    password = request.form.get('password', '')
    result = None
    global current_user_id  # Используем глобальную переменную

    if username and password:
        with sqlite3.connect (PASSWORD_DB) as con:
            cur = con.cursor()
            cur.execute("""SELECT * FROM users""")
            user_list = cur.fetchall()
            for user in user_list:
                if user[1] == username and user[2] == password:
                    current_user_id = user[0]
                    result = True
                else:
                    result = False
    return render_template('test2_login.html', result=result)

@app.route('/feed/', methods=['GET', 'POST'])
def feed_page():
    with sqlite3.connect (PASSWORD_DB) as con:
        cur = con.cursor()
        cur.execute("""SELECT users.name, description, image
                    FROM posts
                    JOIN users ON users.id = posts.user_id""")
        publications = cur.fetchall()
    if not publications:
        publications = []
    return render_template('test2_feed_SQL.html', publications=publications)

@app.route('/load/', methods=['GET', 'POST'])
def load_page():
    if request.method == 'POST':
        descript = request.form.get('description', '')  # Получить описание
        file = request.files.get('file')  # Получить файл изображения

        if file:
            # Сохраняем файл и публикацию
            filename = file.filename
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(filepath)

            with sqlite3.connect (PASSWORD_DB) as con:
                cur = con.cursor()
                cur.execute(
                    "INSERT INTO posts (user_id, description, image) VALUES (?, ?, ?)",
                    (current_user_id, descript, filename)
                )

        return redirect(url_for('feed_page'))
    return render_template('test2_load_SQL.html')


if __name__ == ('__main__'):
    app.run (debug=True)
    # app.run (host='0.0.0.0', port=5000)

