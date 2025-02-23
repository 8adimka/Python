# В этом задании Вам предстоит протестировать 
# несколько функций использующих базу данных.
# 
# Код по запуску flask-приложения и самой базы данных мы намеренно
# не включали в этот пример, чтобы Вы смогли на деле воспользоваться функционалом мок,
# предоставляемым пакетом Unittest. Здесь сами по себе методы возвращающие объекты из БД
# не будут работать, так как у нас просто напросто нет 
# базы данных, к которой можно подключиться.
#
# Попробуем реализовать простой приём, позволяющий протестировать код без базы данных.
# ----------------------------------------------------------------------
# Для использования мока в данном примере необходимо вспомнить
# базовые функции для запроса объектов из базы данных
# структуры класса db.Model пакета flask_sqlalchemy.
# Представим, что наша модель называется User
#
# Для получения всех объектов из базы используем метод User.query.all()
# Для получения одного объекта используем метод User.query.get(id)
#
# Для начала нам этого хватит
# ------------------------------------------------------------------------
#
# Итак что нам нужно сделать несколько фикстур:
# 1. Создадим словарик с базой данных
# 2. Переопределить необходимые методы, которые использует модель User
#
# Разделим задание на действия:
# 1. Сперва от Вас требуется написать фикстуру, которая будет нашими данными в базе.
#    В этой фикстуре всё как обычно, создаём записи в базе данных:
#    u1 = User(id=1, first_name='Иван', last_name='Иванович', email='vanya@skypro.com')
#    u2 = User(id=2, first_name='Петр', last_name='Петрович', email='petya@skypro.com')
#    u3 = User(id=3, first_name='Тест', last_name='Тестович', email='testya@skypro.com')
#    А возвращать фикстура будет словарик в котором в качестве 
#    ключа продублируем id пользователей в таком виде:
#    {1: UserObject, 2: UserObject}
#     
#
# 2. Создаём фикстуру, которая мокает модель юзера.
#    * Она должна принимать наш словарик.
#    * Она должна содержать:
#      - переменную user c сылкой на сам класс User
#      - заглушку для user.query
#      - заглушку для метода user.query.all, который 
#        будет возвращать нам все значения словарика,
#        этого можно добиться, вызвав у словаря метод values, 
#        который вернёт нам все значения в виде списка)
#      - заглушку для метода user.query.get(id) - который бы 
#        по id возвращал нам конкретного пользователя. Для этого
#        воспользуйтесь именованным аргументом side_effect 
#        при инициализации класса MagicMock, передав ему 
#        метод get нашего словарика, но не вызывайте его сразу.)
# 
# P.S. В этом задании мы уже написали тесты за Вас, 
# попробуйте воспользоваться Мок и фикстурами так,
# чтобы тестируемые функции сработали как на настоящей БД.
#
#
# ИСХОДНЫЙ КОД и отсутствующая база данных
from flask_sqlalchemy import SQLAlchemy
from unittest.mock import MagicMock
import pytest
import os
db = SQLAlchemy()

class User(db.Model):
    __tablename__ = 'books'
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String)
    last_name = db.Column(db.String)
    email = db.Column(db.String)

def get_users():
    users = User.query.all()
    result = ", ".join([f"{user.first_name} {user.last_name}" for user in users])
    return f"Наши пользователи {result}"

def get_profile(uid):
    user = User.query.get(uid)
    first_name = user.first_name
    last_name = user.last_name
    return f"Профиль пользователя: {first_name} {last_name}"
# КОНЕЦ ИСХОДНОГО КОДА.

@pytest.fixture
def test_objects():
    test_user1 = User(id=1, first_name='Иван', last_name='Иванович', email='vanya@skypro.com')
    test_user2 = User(id=2, first_name='Петр', last_name='Петрович', email='petya@skypro.com')
    test_user3 = User(id=3, first_name='Тест', last_name='Тестович', email='testya@skypro.com')
    return {1: test_user1, 2: test_user2, 3: test_user3}

@pytest.fixture
def user(test_objects):
    user = User
    user.query = MagicMock()
    user.query.all = MagicMock(return_value=test_objects.values())
    user.query.get = MagicMock(side_effect=test_objects.get)
    return user

# Не изменяйте пожалуйста эти тесты. 
# Если вы правильно сделаете фикстуры, они завершатся успешно.
#
def test_get_users(user: None):
    expected = "Наши пользователи Иван Иванович, Петр Петрович, Тест Тестович"
    assert get_users() == expected

def test_get_profile(user: None):                               # Если мы добавляем здесь аргумент user,
    expected = "Профиль пользователя: Иван Иванович"      # то наша реальная модель User заменяется фикстурой
    assert get_profile(1) == expected


if __name__ =="__main__":
    os.system("pytest")