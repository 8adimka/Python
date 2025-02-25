# Таблица сообщений
# Создайте модель Course по таблице course:
# +----+-------------------+---------+-------+-------+
# | id |       title       | subject | price | weeks |
# +----+-------------------+---------+-------+-------+
# | 1  | Введение в Python |  Python | 11000 |  3.5  |
# | 2  |  Пишем на Spring  |   Java  | 15000 |  8.0  |
# | 3  |   Игры на Python  |  Python | 13500 |  5.0  |
# | 4  |    Игры на Java   |   Java  |  9000 |  4.5  |
# +----+-------------------+---------+-------+-------+
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


class Course(db.Model):
    __tablename__ = 'course'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String)
    subject = db.Column(db.String)
    price = db.Column(db.Integer)
    weeks = db.Column(db.Float)

with app.app_context():
    db.create_all()

    courses = [
        Course(title="Введение в Python", subject="Python", price=11000, weeks=3.5),
        Course(title="Пишем на Spring", subject="Java", price=15000, weeks=8.0),
        Course(title="Игры на Python", subject="Python", price=13500, weeks=5.0),
        Course(title="Игры на Java", subject="Java", price=9000, weeks=4.5),
    ]

    db.session.add_all(courses)
    db.session.commit()


    session = db.session()
    cursor = session.execute(text(f"SELECT * from {Course.__tablename__}")).cursor
    mytable = prettytable.from_db_cursor(cursor)
    mytable.max_width = 30


if __name__ == '__main__':
    print(mytable)
