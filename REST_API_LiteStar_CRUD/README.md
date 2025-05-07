REST API для управления пользователями на LiteStar
Полноценное приложение с CRUD-операциями для пользователей, используя LiteStar и PostgreSQL. 
1. Полная структура проекта:

/home/v/Python/REST_API_LiteStar_CRUD/
├── .env
├── .gitignore
├── docker-compose.yml
├── pyproject.toml
├── README.md
└── src/
    ├── __init__.py
    ├── db/
    │   ├── __init__.py
    │   ├── models.py
    │   └── session.py
    ├── domain/
    │   ├── __init__.py
    │   └── users/
    │       ├── __init__.py
    │       ├── controllers.py
    │       ├── dtos.py
    │       ├── models.py
    │       ├── repository.py
    │       └── service.py
    ├── lib/
    │   ├── __init__.py
    │   └── settings.py
    └── server.py

2. Запустите приложения:

bash
docker-compose up -d
Приложение будет доступно по адресу http://localhost:8000/api/docs
(Swagger UI)

3. Проверка работоспособности:
curl -v http://localhost:8000/users

docker-compose logs app

Создание пользователя:

POST /users

Body:

json
{
  "name": "John",
  "surname": "Doe",
  "password": "securepassword123"
}

curl -X POST "http://localhost:8000/users" \
-H "Content-Type: application/json" \
-d '{"name": "John", "surname": "Doe", "password": "secure123"}'

Получение списка пользователей:

GET /users

Получение одного пользователя:

GET /users/1

Обновление пользователя:

PUT /users/1

Body:

json
{
  "name": "John Updated"
}
Удаление пользователя:

DELETE /users/1

С осторожностью, по необходимости:
docker-compose down -v
docker system prune -a

4. Особенности реализации
Использован Advanced-SQLAlchemy для работы с базой данных

Реализована полная валидация входных данных

Настроен Swagger UI для документации API

Использованы современные практики Python (типизация, async/await)

Приложение готово к развертыванию