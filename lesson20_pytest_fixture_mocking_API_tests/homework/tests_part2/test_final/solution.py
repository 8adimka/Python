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


def test_get_users(user):
    expected = "Наши пользователи Иван Иванович, Петр Петрович, Тест Тестович"
    assert get_users() == expected

def test_get_profile(user):
    expected = "Профиль пользователя: Иван Иванович"
    assert get_profile(1) == expected


if __name__ =="__main__":
    os.system("pytest")