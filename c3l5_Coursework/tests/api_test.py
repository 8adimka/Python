import pytest, os, sys
import json
from flask import Flask


from app.api.views import api_blueprint  # Импортируем только api_blueprint из нашего приложения

@pytest.fixture
def client():
    # Создаём тестовое приложение Flask
    app = Flask(__name__)
    app.config['TESTING'] = True  # Включаем тестовый режим

    # Регистрируем только api_blueprint
    app.register_blueprint(api_blueprint)

    # Создаём тестовый клиент для выполнения запросов
    with app.test_client() as client:
        yield client

def test_posts(client):
    
    # Отправляем GET-запрос к маршруту
    response = client.get('/api/posts/')
    
    # Проверяем статус-код ответа
    assert response.status_code == 200

    # Загружаем ожидаемые данные из JSON-файла
    file_path = '/home/v/Python/c3l5_Coursework/static/data/posts.json'
    with open(file_path, 'r', encoding='utf-8') as f:
        posts_data = json.load(f)
        
        for post in posts_data:
            # Разделяем текст в 'content' на список слов
            content_list = post['content'].split()
            
            # Отбираем хэштеги
            hashtags = ' '.join([word for word in content_list if word.startswith('#')])
            
            # Убираем хэштеги из текста
            content = ' '.join([word for word in content_list if not word.startswith('#')])
            
            # Обновляем словарь поста
            post['hashtags'] = hashtags
            post['content'] = content

    # Проверяем, что ответ соответствует ожидаемым данным
    assert response.json == posts_data