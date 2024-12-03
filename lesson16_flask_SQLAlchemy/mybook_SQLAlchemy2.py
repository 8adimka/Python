from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
import os

app = Flask (__name__)

UPLOAD_FOLDER = '/home/v/Python/lesson16_flask_SQLAlchemy/static/uploads'  # путь к папке для сохранения изображений
PASSWORD_DB = '/home/v/Python/lesson16_flask_SQLAlchemy/my_book.db'

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

app.config['SQLALCHEMY_DATABASE_URI'] = f"sqlite:///{PASSWORD_DB}"
db = SQLAlchemy(app)

# Объявляем таблицы для БД 
class User (db.Model):
    __tablename__ = "users"
    id = db.Column (db.Integer, primary_key = True, autoincrement = True)
    name = db.Column (db.String (100))
    password = db.Column(db.String(255))

class Posts (db.Model):
    __tablename__ = "posts"
    id = db.Column (db.Integer, primary_key = True)
    username = db.Column (db.String (100))
    description = db.Column(db.String(1000))
    image = db.Column(db.String(1000))

# Удаляем все уже созданные таблицы, в случае если решили поменять модель
# db.drop_all()

# Создаём все объявленные выше таблицы в базе данных, если они отсутствуют
with app.app_context():
    db.create_all()

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
    username = request.form.get('username', '').lower()
    user_password = request.form.get('password', '')
    result = None

    if username and user_password:
        new_user = User(name=username,password=user_password)
        try:
            db.session.add(new_user)
            db.session.commit()
            result = True
        except Exception:
            db.session.rollback()
            result = False

    return render_template('test2_registr.html', result=result)

@app.route('/login/', methods=['GET', 'POST'])
def user_password():
    username = request.form.get('username', '').lower()
    password = request.form.get('password', '')
    result = None

    if username and password:
        user_list = User.query.all()
        for user in user_list:
            if user.name == username and user.password == password:
                result = True
            else:
                result = False
    return render_template('test2_login.html', result=result)

@app.route('/feed/', methods=['GET', 'POST'])
def feed_page():
    publications = Posts.query.all()
    if not publications:
        publications = []
    return render_template('test2_feed.html', publications=publications)

@app.route('/load/', methods=['GET', 'POST'])
def load_page():
    if request.method == 'POST':
        name = request.form.get('username', 'Аноним')  # Получить логин пользователя
        descript = request.form.get('description', '')  # Получить описание
        file = request.files.get('file')  # Получить файл изображения

        if file:
            # Сохраняем файл и публикацию
            filename = file.filename
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(filepath)

            new_post = Posts (username=name, description=descript, image=filename)
            try:
                db.session.add(new_post)
                db.session.commit()

            except Exception:
                db.session.rollback()

        return redirect(url_for('feed_page'))
    return render_template('test2_load.html')


if __name__ == ('__main__'):
    app.run (debug=True)
    # app.run (host='0.0.0.0', port=5000)

