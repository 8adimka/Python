# Имеется наполненная БД с таблицей guide и полуготовый код на фласке.
# Напишите представления для следующих ендпоинтов:
#
# Method: GET
# URL: /guides
# Response: [{guide_json}, {guide_json}, {guide_json}]
#
# Method: GET
# URL: /guides/1
# Response: { <guide_json> }
#
import json
from flask import Flask, jsonify
from sqlalchemy import text
from flask_sqlalchemy import SQLAlchemy
from guides_sql import CREATE_TABLE, INSERT_VALUES

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['JSON_AS_ASCII'] = False
app.url_map.strict_slashes = False
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


@app.route("/")
def get_guides():
    with app.app_context():
        guides = Guide.query.all()
        response = [{'id' : guide.id, 'surname' : guide.surname, 'tours_count' : guide.tours_count} for guide in guides]
    
    return json.dumps(response, ensure_ascii=False)  # <-- Включаем поддержку UTF-8


@app.route("/g/<int:gid>/")
def get_guide(gid):
    with app.app_context():
        guide = Guide.query.get(gid)
        response = {'id' : guide.id, 'surname' : guide.surname, 'tours_count' : guide.tours_count}
    
    return json.dumps(response, ensure_ascii=False)  # <-- Включаем поддержку UTF-8


if __name__ == "__main__":
    app.run()
