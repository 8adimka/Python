FROM python:3.12-slim

WORKDIR /app

# Устанавливаем системные зависимости
RUN apt-get update && apt-get install -y \
    gcc \
    python3-dev \
    && rm -rf /var/lib/apt/lists/*

# Копируем требования и конфигурационные файлы
COPY requirements.txt alembic.ini ./

# Устанавливаем зависимости
RUN pip install --upgrade pip && \
    pip install --no-warn-script-location -r requirements.txt

# Копируем исходный код
COPY src /app/src

# Устанавливаем PYTHONPATH
ENV PYTHONPATH=/app/src

CMD ["uvicorn", "src.server:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]
