from datetime import timedelta

# Настройки времени
MIN_DELAY = 1.5
MAX_DELAY = 4.0
WAIT_TIMEOUT = 20
LONG_DELAY = 100

# Настройки ограничений
MAX_RETRIES = 30
RATE_LIMIT_DELAY = 600  # 10 минут при 429 ошибке
RECOVERY_CHECK_INTERVAL = 300  # 5 минут в режиме восстановления


