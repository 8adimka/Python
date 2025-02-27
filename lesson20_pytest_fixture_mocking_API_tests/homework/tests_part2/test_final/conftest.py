import pytest
from unittest.mock import MagicMock
from test_final import User, db

@pytest.fixture
def test_objects():
    test_user1 = User(id=1, first_name='Иван', last_name='Иванович', email='vanya@skypro.com')
    test_user2 = User(id=2, first_name='Петр', last_name='Петрович', email='petya@skypro.com')
    test_user3 = User(id=3, first_name='Тест', last_name='Тестович', email='testya@skypro.com')
    return {1: test_user1, 2: test_user2, 3: test_user3}

@pytest.fixture
def user(test_objects):
    # Мокируем методы запросов
    user_query = MagicMock()
    user_query.all = MagicMock(return_value=list(test_objects.values()))
    user_query.get = MagicMock(side_effect=test_objects.get)

    # Заменяем query у модели User
    User.query = user_query
    return User

