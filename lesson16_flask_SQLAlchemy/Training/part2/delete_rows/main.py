# Напишите функцию delete_guides, которая
# удаляет из базы гидов c id = 1,4,7
#
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import prettytable
from sqlalchemy import text, or_
from guides_sql import CREATE_TABLE, INSERT_VALUES

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
with app.app_context():
    db.session.execute(text(CREATE_TABLE))
    db.session.execute(text(INSERT_VALUES))
    db.session.commit()


class Guide(db.Model):
    __tablename__ = 'guide'
    id = db.Column(db.Integer, primary_key=True)
    surname = db.Column(db.String)
    full_name = db.Column(db.String)
    tours_count = db.Column(db.Integer)
    bio = db.Column(db.String)
    is_pro = db.Column(db.Boolean)
    company = db.Column(db.Integer)


def delete_guides():
    with app.app_context():
        # db.session.query(Guide).filter(or_(Guide.id == 1,Guide.id == 4,Guide.id == 7)).delete()
        # db.session.query(Guide).filter(Guide.id.notin_([2,3,5,6,8])).delete()
        db.session.query(Guide).filter(Guide.id.in_([1,4,7])).delete()
        db.session.commit()

with app.app_context():
    delete_guides()
    session = db.session()
    cursor = session.execute(text("SELECT * FROM guide")).cursor
    mytable = prettytable.from_db_cursor(cursor)
    mytable.max_width = 30

if __name__ == '__main__':
    print('БАЗА ДАННЫХ:')
    print(mytable)
