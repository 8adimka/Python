# Напишите функцию update_tours_count, которая
# обновит значение поля tours_count до 6 у гида
# c id = 1
#
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import prettytable
from sqlalchemy import text
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


def update_tours_count(id, n):
    with app.app_context():
        guide = Guide.query.get(id)
        guide.tours_count = n
        db.session.add(guide)
        db.session.commit()

# не удаляйте код ниже, он необходим
# для выдачи результата запроса

with app.app_context():
    update_tours_count(id=1, n=6)
    ses = db.session()
    cursor = ses.execute(text("SELECT * FROM guide WHERE `id`=1")).cursor
    mytable = prettytable.from_db_cursor(cursor)
    mytable.max_width = 30

if __name__ == '__main__':
    print(mytable)
