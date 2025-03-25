FROM python:3.11-slim

WORKDIR /app

# Копируем зависимости первыми для кэширования
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Копируем остальные файлы
COPY . .

# Переменные окружения
ENV PYTHONDONTWRITEBYTECODE=1
# Автоматическая запись логов
ENV PYTHONUNBUFFERED=1

CMD ["python", "main.py"]
