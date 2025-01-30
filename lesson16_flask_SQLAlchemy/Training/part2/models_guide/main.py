# Допишите модели гид(Guide) экскурсия (Excursion)
# в соответствии с ulm (схема расположена в корне папки задания)
#
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import prettytable
from sqlalchemy.orm import relationship
from sqlalchemy import text

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db: SQLAlchemy = SQLAlchemy(app)


class Guide(db.Model):
    __tablename__ = 'guide'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String (100))
    main_speciality = db.Column(db.String(200))
    country = db.Column(db.String(100))
    excursions = relationship ("Excursion", back_populates='guide')

class Excursion(db.Model):
    __tablename__ = 'excursion'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String (100))
    guide_id = db.Column(db.Integer, db.ForeignKey('guide.id'))
    guide = relationship ("Guide", back_populates='excursions')

# Не удаляйте код ниже, он нужен для корректного
# отображения созданной вами модели

with app.app_context():
    db.create_all()
    db.session.add(Excursion(name='Cartahena', guide=Guide(name='Елена Либерман', country='Spain')))
    db.session.commit()
    session = db.session()
    cursor_guide = session.execute(text("SELECT * from guide")).cursor
    mytable = prettytable.from_db_cursor(cursor_guide)
    cursor_excursion = session.execute(text("SELECT * from excursion")).cursor
    mytable2 = prettytable.from_db_cursor(cursor_excursion)


if __name__ == '__main__':
    print(mytable)
    print(mytable2)
