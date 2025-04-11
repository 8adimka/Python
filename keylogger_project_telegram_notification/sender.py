import os
import logging
from config import TELEGRAM_BOT_TOKEN, TELEGRAM_CHAT_ID, LOG_FILE_PATH
from telegram import Bot
from telegram.error import TelegramError

# Установим логгирование
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def send_log():
    if not os.path.exists(LOG_FILE_PATH):
        logger.warning("Файл логов не найден.")
        return

    bot = Bot(token=TELEGRAM_BOT_TOKEN)

    try:
        # Отправка файла (удобно, если лог большой)
        with open(LOG_FILE_PATH, "rb") as f:
            bot.send_document(chat_id=TELEGRAM_CHAT_ID, document=f, filename="log.txt")
        logger.info("Логи успешно отправлены.")

        # Очистка логов после отправки
        with open(LOG_FILE_PATH, "w", encoding="utf-8") as f:
            f.write("")  # очищаем файл
        logger.info("Файл логов очищен.")

    except TelegramError as e:
        logger.error(f"Ошибка при отправке в Telegram: {e}")
        