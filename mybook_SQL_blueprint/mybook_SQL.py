from flask import Flask, session, request_started
import os, sqlite3

from enter.views import enter_blueprint
from start.views import start_blueprint
from registr.views import registr_blueprint
from login.views import login_blueprint
from feed.views import feed_blueprint
from load.views import load_blueprint
from search.views import search_blueprint


app = Flask (__name__)
app.secret_key = '1911'  # Необходимо для использования сессий

UPLOAD_FOLDER = '/home/v/Python/c3l3_blueprint/mybook_SQL_blueprint/static/uploads'  # путь к папке для сохранения изображений
PASSWORD_DB_PATH = '/home/v/Python/c3l3_blueprint/mybook_SQL_blueprint/my_book_SQL.db'

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['PASSWORD_DB_PATH'] = PASSWORD_DB_PATH

# Создаём папку для загрузок, если её нет
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

# Подключение к базе данных и создание таблиц
def initialize_database():
    try:
        with sqlite3.connect(PASSWORD_DB_PATH) as con:
            cur = con.cursor()
            query = """
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name VARCHAR (100),
                password VARCHAR (250)
            );

            CREATE TABLE IF NOT EXISTS posts (
                post_id INTEGER PRIMARY KEY,
                user_id INTEGER,
                description TEXT,
                image VARCHAR (350),
                FOREIGN KEY (user_id) REFERENCES users(id)
            );
            """
            cur.executescript(query)
    except sqlite3.Error as e:
        print(f"Ошибка при подключении к базе данных: {e}")

initialize_database()

@app.before_request
def ensure_user_id():
    if 'user_id' not in session:
        session['user_id'] = None

def clear_sessions_on_startup(sender, **extra):
    if not hasattr(app, '_session_cleared'):
        session.clear()
        app._session_cleared = True

request_started.connect(clear_sessions_on_startup, app)

# Регистрация Blueprints
app.register_blueprint (start_blueprint)
app.register_blueprint (enter_blueprint)
app.register_blueprint (registr_blueprint)
app.register_blueprint (login_blueprint)
app.register_blueprint (feed_blueprint) 
app.register_blueprint (load_blueprint)
app.register_blueprint (search_blueprint)

if __name__ == ('__main__'):
    app.run (debug=True)
    # app.run (host='0.0.0.0', port=5000)
