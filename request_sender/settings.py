from datetime import timedelta

PERSONAL_DATA = {
    'txtIdCitado': 'Z1377887P',
    'txtDesCitado': 'VADIM MEDINTSEV',
    'txtAnnoCitado': '1991',
    'txtPaisNac': 'RUSIA'
}

# Настройки времени
MIN_DELAY = 1.5
MAX_DELAY = 4.0
WAIT_TIMEOUT = 20
LONG_DELAY = 100

# Настройки ограничений
MAX_RETRIES = 30
RATE_LIMIT_DELAY = 600  # 10 минут при 429 ошибке
RECOVERY_CHECK_INTERVAL = 300  # 5 минут в режиме восстановления

# Telegram
TELEGRAM_BOT_TOKEN = "7742964123:AAHJD1pCEu4xCKmYrZFUY-RPR2gQMYp3z8o"
TELEGRAM_CHAT_ID = 1839026469
