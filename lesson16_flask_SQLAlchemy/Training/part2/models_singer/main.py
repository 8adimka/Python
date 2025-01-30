# Напишите модель певец (Singer) с именем таблицы "singer"
# Для данной модели заданы следующие ограничения:
#
#
# #Таблица singer, описание колонок:
# Идентификатор - первичный ключ (PK) - id
# Имя - должно быть уникальным - name
# Возраст - не больше 35 лет - age
# Группа - не может быть Null (None) - group
#
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import prettytable
from sqlalchemy import text

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


class Singer(db.Model):
    __tablename__ = 'singer'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, unique=True)
    age = db.Column(db.Integer, db.CheckConstraint('age<=35'))
    group = db.Column(db.String(200), nullable=False)


with app.app_context():
    db.drop_all()
    db.create_all()
    db.session.add(Singer(name='Антошка Картошка', age=34, group='Бременские музыканты'))
    db.session.commit()
    session = db.session()
    cursor = session.execute(text("SELECT * from singer")).cursor
    mytable = prettytable.from_db_cursor(cursor)
    session.close()

if __name__ == '__main__':
    print(mytable)
