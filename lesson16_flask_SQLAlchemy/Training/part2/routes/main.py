# УРОК 16 Задание 8
# В этом финальном задании вам нужно
# применить знания о моделях для создания 3 представлений,
# которые реализуют запросы на создание, добавление, удаление.

"""
    # Задание
    # Шаг 1.
    # ######
    # Создайте представение для эндпоинта GET /guides
    # которое возвращает список всех гидов со всеми полями
    # в формате JSON
    #
    #
    # Шаг 2.
    # ######
    # - Создайте представение для эндпоинта GET /guides/{id}
    # которое возвращает одного гида со всеми полями
    # в формате JSON в соответствии с его id
    #
    # Шаг 3.
    # ######
    # Создайте представение для эндпоинта
    # GET /guides/{id}/delete`, которое удаляет
    # одного гида в соответствии с его `id`
    #
    # Шаг 4.
    # ######
    # Создайте представление для эндпоинта POST /guides
    #  которое добавляет в базу данных гида, при получении
    # следующих данных:
    # {
    #     "surname": "Иванов",
    #     "full_name": "Иван Иванов",
    #     "tours_count": 7,
    #     "bio": "Провожу экскурсии",
    #     "is_pro": true,
    #     "company": "Удивительные экскурсии"
    # }
    # Шаг 5.
    # ######
    # - Допишите представление из шага 1 для фильтрации так,
    # чтобы при получении запроса типа /guides?tours_count=1
    # возвращались гиды с нужным количеством туров.
"""

from flask import Flask, request
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import text
from guides_sql import CREATE_TABLE, INSERT_VALUES
import json

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

@app.route('/')
def get_guides ():
    with app.app_context():
        tours_count = request.args.get('tours_count')
        if tours_count:
            guides = db.session.query(Guide).filter(Guide.tours_count == tours_count)
        else:
            guides = Guide.query.all()
            # response = [{'id' : guide.id, 'surname' : guide.surname, 'tours_count' : guide.tours_count} for guide in guides]
        response = [{k: v for k, v in guide.__dict__.items() if not k.startswith('_')} for guide in guides]
        return json.dumps(response, ensure_ascii=False)

@app.route('/<int:id>/')
def get_guide_id(id):
    with app.app_context():
        guide = db.session.query(Guide).get(id)
        if guide:
            response = {k:v for k,v in guide.__dict__.items() if not k.startswith('_')}
            return json.dumps(response, ensure_ascii=False)
    return 'Данный пользователь не найден!'

@app.route('/delete/<int:sid>')
def delete_guide_id(sid):
    with app.app_context():
        try:
            db.session.query(Guide).filter(Guide.id==sid).delete()
            db.session.commit()
            return "Пользователь удалён"
        except Exception as e:
            db.session.rollback()
            print (f'Error: {e}, \nПользователь не найден!')

@app.route('/guide/', methods=['POST', 'GET'])
def create_guide():
    with app.app_context():
        try:
            new_guide = Guide(**{
            "surname": "Иванов",
            "full_name": "Иван Иваныч",
            "tours_count": 7,
            "bio": "Провожу экскурсии",
            "is_pro": True,
            "company": "Удивительные экскурсии"})
            db.session.add(new_guide)
            db.session.commit()
            return 'Пользователь добавлен'
        except Exception as e:
            print (f'Error {e} - cant add new_guide')
            db.session.rollback()
            return 'Пользователь НЕ добавлен'




if __name__ == "__main__":
    app.run()
