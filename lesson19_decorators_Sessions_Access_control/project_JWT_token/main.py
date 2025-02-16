# project/
# │── app/
# │──│── dao/                 Data Access Object - обьект для получения данных
# │──│──│── models/           Определение моделей SQLAlchemy
# │──│──│──│──__init__.py     Чтобы Python видел папку как модуль  
# │──│──│──│──directors.py
# │──│──│──│──genres.py
# │──│──│──│──movies.py
# │──│──│──│──users.py

# │──│──│──__init__.py
# │──│──│──directors.py       DAO выполняют работу с базами данных, 
# │──│──│──genres.py          получают из неё данные
# │──│──│──movies.py
# │──│──│──users.py

# │──│── services/            Вся бизнес-логика приложения
# │──│──│──__init__.py        что обновлять, как обновлять, где создавать, где удалять и т.д.
# │──│──│──directors.py
# │──│──│──genres.py
# │──│──│──movies.py
# │──│──│──users.py

# │──│── views/                Вьюшки
# │──│──│──__init__.py 
# │──│──│──directors.py
# │──│──│──genres.py
# │──│──│──movies.py
# │──│──│──users.py

# │──│──__init__.py            Чтобы Python видел папку как модуль         
# │──│──config.py              Конфигурация Flask
# │──│──container.py           Service-container. Все слои связываются путём контейнера(модели->DAO->сервисы->контейнер и во views делаем импорт св.сервисов из контейнера)
# │──│──database.py            Настройка БД
# │──│──create_database.py     Заполнение данными
# │──│──constants.py           Это файл для глобальных констант. Вместо 'C:\\Windows' в коде, лучше создайть константу WINDOWS_PATH здесь и присвоить ей значение.
# │──│──user_auth_jwt.py   

# │──main.py                   Основной файл с эндпоинтами
# │──__init__.py               Чтобы Python видел папку как модуль

from flask import Flask
from flask_restx import Api
from app.config import Config
from app.database import db
from app.create_database import init_db
from app.views.movies import movies_ns
from app.views.directors import directors_ns
from app.views.genres import genres_ns
from app.views.users import users_ns

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
    api.add_namespace(users_ns)


if __name__ == '__main__':
    app_config = Config()
    app = create_app(app_config)
    configure_app(app)
    init_db(app) # Создание базы данных
    app.run(debug=True)
