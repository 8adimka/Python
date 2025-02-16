# project/
# │── app/
# │──│── views/                Вьюшки
# │──│──│──__init__.py 
# │──│──│──directors.py
# │──│──│──genres.py
# │──│──│──movies.py
# │──│──__init__.py            Чтобы Python видел папку как модуль         
# │──│──config.py              Конфигурация Flask
# │──│──models.py              Определение моделей SQLAlchemy
# │──│──database.py            Настройка БД
# │──│──create_database.py     Заполнение данными
# │──main.py                   Основной файл с эндпоинтами 
# │──__init__.py               Чтобы Python видел папку как модуль

from flask import Flask, request
from flask_restx import Api, Resource
from sqlalchemy import ForeignKey
from app.config import Config
from app.database import db
from app.create_database import init_db
from app.views.movies import movies_ns
from app.views.directors import directors_ns
from app.views.genres import genres_ns

def create_app(config: Config) -> Flask:
    application = Flask(__name__)
    application.config.from_object(config)
    application.app_context().push()

    return application

def configure_app(application: Flask):
    db.init_app(application)
    api = Api(app)
    api.add_namespace(movies_ns)
    api.add_namespace(directors_ns)
    api.add_namespace(genres_ns)




if __name__ == '__main__':
    app_config = Config()
    app = create_app(app_config)
    configure_app(app)
    init_db(app) # Создание базы данных
    app.run(debug=True)
