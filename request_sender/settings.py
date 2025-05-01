from datetime import timedelta
from dotenv import load_dotenv
import os
import ast

# Загружаем переменные из .env
load_dotenv()

# Получаем PERSONAL_DATA из .env
PERSONAL_DATA = ast.literal_eval(os.getenv('PERSONAL_DATA'))

# Настройки времени
MIN_DELAY = 1.5
MAX_DELAY = 4.0
WAIT_TIMEOUT = 20

# Настройки ограничений
MAX_RETRIES = 50
RATE_LIMIT_DELAY = 600  # 10 минут при 429 ошибке
RECOVERY_CHECK_INTERVAL = 300  # 5 минут в режиме восстановления

# Telegram (берём из .env)
TELEGRAM_BOT_TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')
TELEGRAM_CHAT_ID = int(os.getenv('TELEGRAM_CHAT_ID'))
