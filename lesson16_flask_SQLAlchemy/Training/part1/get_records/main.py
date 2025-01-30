# Имеется модель и заполненная база данных.
# 1. Напишите функцию get_all() которая будет возвращать все объекты из базы
# 2. Напишите функцию get_one() которая будет принимать аргумент id и
#  возвращать объект из базы, в соответствии с полученным аргументом.
#

from flask import Flask
from sqlalchemy import text
from flask_sqlalchemy import SQLAlchemy
import prettytable
from users_sql import CREATE_TABLE, INSERT_VALUES

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Используем контекст приложения для работы с базой данных
with app.app_context():
    # Создаём таблицу и добавляем данные
    db.session.execute(text(CREATE_TABLE))
    db.session.execute(text(INSERT_VALUES))
    db.session.commit()


class User(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String)
    password = db.Column(db.String)
    full_name = db.Column(db.String)
    city = db.Column(db.Integer)
    city_ru = db.Column(db.String)


def get_all():
    # Получаем все объекты из базы внутри контекста приложения
    with app.app_context():
        users = User.query.all()

        # Создаём prettytable и добавляем данные
        table = prettytable.PrettyTable()
        table.field_names = ['id', 'email', 'password', 'full_name', 'city', 'city_ru']
        
        for user in users:
            table.add_row([user.id, user.email, user.password, user.full_name, user.city, user.city_ru])
        
        return table


def get_one(id):
    # Получаем один объект по id внутри контекста приложения
    with app.app_context():
        user = User.query.get(id)

        # Создаём prettytable и добавляем данные
        table = prettytable.PrettyTable()
        table.field_names = ['id', 'email', 'password', 'full_name', 'city', 'city_ru']
        
        if user:
            table.add_row([user.id, user.email, user.password, user.full_name, user.city, user.city_ru])
        
        return table


if __name__ == '__main__':

    # Пример использования

    print("Все пользователи:")
    print(get_all())

    # Получение одного пользователя
    print("\nПользователь с id 1:")
    print(get_one(1))


