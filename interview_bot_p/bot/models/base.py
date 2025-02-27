from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine

# Создаем базовый класс для всех моделей
Base = declarative_base()

# Настройка сессии (если нужно)
# engine = create_engine('DATABASE_URL')  # Укажите URL вашей базы данных
# Session = sessionmaker(bind=engine)
