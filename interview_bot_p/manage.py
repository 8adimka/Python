# interview_bot/
# ├── .env                        # Файл с переменными окружения
# ├── .gitignore
# ├── bot/                        # Основное приложение (Django app)
# │   ├── management/             # Кастомные команды управления
# │   │   ├── __init__.py
# │   │   ├── commands/
# │   │   │   ├── __init__.py
# │   │   │   ├── add_initial_data.py
# │   │   │   ├── add_prompts.py  # Команда для добавления промптов
# │   ├── controllers/            # Обработчики команд бота
# │   │   ├── __init__.py
# │   │   ├── command.py
# │   │   ├── start_handler.py    # Обработчик команды /start
# │   │   ├── voice_handler.py    # Обработчик голосовых сообщений
# │   ├── services/               # Сервисный слой (бизнес-логика)
# │   │   ├──dto/                    # Data Transfer Objects (DTO)
# │   │   │   ├── __init__.py
# │   │   │   ├── gpt_request.py      # DTO для запроса к GPT
# │   │   │   ├── gpt_response.py     # DTO для ответа от GPT
# │   │   │   ├── question.py         # DTO для вопроса
# │   │   │   ├── transcription.py    # DTO для транскрипции
# │   │   ├── __init__.py
# │   │   ├── gpt_client.py
# │   │   ├── openai_client.py    # Клиент для работы с OpenAI API
# │   │   ├── question_service.py # Сервис для работы с вопросами
# │   ├── dao/                    # Data Access Object (доступ к данным)
# │   │   ├── __init__.py
# │   │   ├── answer_dao.py
# │   │   ├── question_dao.py
# │   │   ├── interview_repository.py  # Репозиторий для вопросов и ответов
# │   │   ├── topic_repository.py      # Репозиторий для тем собеседования
# │   │   ├── prompt_dao.py            # DAO для работы с текстовыми шаблонами
# │   ├── models/                 # Модели базы данных
# │   │   ├── __init__.py
# │   │   ├── question.py         # Модель для вопросов
# │   │   ├── answer.py           # Модель для ответов
# │   │   ├── prompt.py           # Модель для текстовых шаблонов
# │   ├── views.py                # Django views (если понадобятся)
# │   ├── urls.py                 # Django URLs (если понадобятся)
# │   ├── telegram_config.py      # Конфигурация Telegram бота
# │   ├── database.py
# │   ├── config.py
# ├── interview_bot/              # Основной проект Django
# │   ├── settings.py             # Настройки Django
# │   ├── urls.py                 # Основные URLs проекта
# │   ├── wsgi.py                 # WSGI-приложение
# ├── manage.py                   # Управление Django-проектом


import os
from bot.database import init_db
from bot.telegram_config import setup_telegram_bot
import sys

sys.path.append(os.path.abspath(os.path.dirname(__file__)))

from bot.management.commands.add_initial_data import Command
    
if __name__ == "__main__":
    # Инициализация базы данных
    init_db()

    # Добавление начальных данных
    command = Command()
    command.handle()

    # Запуск Telegram бота
    token = os.getenv("TELEGRAM_BOT_TOKEN")
    if not token:
        raise ValueError("Переменная окружения TELEGRAM_BOT_TOKEN не установлена.")
    setup_telegram_bot()




