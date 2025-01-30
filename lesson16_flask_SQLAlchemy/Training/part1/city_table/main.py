# Городская таблица
# Определите поля для модели City по таблице city:
# +----+---------+------------+------------+
# | id |   name  | country_ru | population |
# +----+---------+------------+------------+
# | 1  |   Рим   |   Италия   |  2873000   |
# | 2  |  Милан  |   Италия   |  1333000   |
# | 3  | Венеция |   Италия   |   265000   |
# +----+---------+------------+------------+
#
#
import prettytable
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import text

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


class City(db.Model):
    __tablename__ = 'city'
    id = db.Column(db.Integer, primary_key=True)
    name = db.column(db.Text(200))
    country_ru = db.Column(db.Text(200))
    population = db.Column(db.Integer)


with app.app_context():
    db.create_all()

    cities = [
        City(name="Рим", country_ru="Италия", population=2873000),
        City(name="Милан", country_ru="Италия", population=1333000),
        City(name="Венеция", country_ru="Италия", population=265000),
    ]
    db.session.add_all(cities)
    db.session.commit()

    # Извлечение всех данных из таблицы City с помощью SQLAlchemy
    cities_data = City.query.all()

    # Создание таблицы PrettyTable
    mytable = prettytable.PrettyTable()

    # Устанавливаем заголовки для таблицы
    mytable.field_names = ['id', 'name', 'country_ru', 'population']

    # Заполняем таблицу данными
    for city in cities_data:
        mytable.add_row([city.id, city.name, city.country_ru, city.population])

    mytable.max_width = 30


if __name__ == '__main__':
    print(mytable)
