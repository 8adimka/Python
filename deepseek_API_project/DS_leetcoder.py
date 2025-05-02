import time
import random
import pyperclip
import requests
from pynput.keyboard import Controller, Key
import sys
import logging
from typing import Optional
from dotenv import load_dotenv
import os
from pynput import keyboard as kb

# Настройка логирования
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    filename='deepseek_solver.log'
)

keyboard = Controller()

class DeepSeekSolver:
    def __init__(self):
        self.API_URL = "https://api.deepseek.com/v1/chat/completions"
        self.API_KEY = self._get_api_key()
        self.last_request_time = 0
        self.RATE_LIMIT_DELAY = 3  # Задержка между запросами (сек)

    def _get_api_key(self) -> str:
        """Безопасное получение API ключа"""
        # Загружаем переменные из .env
        load_dotenv()
        try: 
            key = os.getenv("DEEPSEEK_API_KEY")
            if not key:
                raise ValueError("API key not found in environment variables")
            return key
        except Exception as e:
            logging.error(f"API key error: {e}")
            sys.exit(1)

    def send_to_api(self, prompt: str) -> Optional[str]:
        """Отправка запроса к API с обработкой ошибок"""
        current_time = time.time()
        if current_time - self.last_request_time < self.RATE_LIMIT_DELAY:
            time.sleep(self.RATE_LIMIT_DELAY - (current_time - self.last_request_time))

        headers = {
            "Authorization": f"Bearer {self.API_KEY}",
            "Content-Type": "application/json"
        }
        
        data = {
            "model": "deepseek-chat",
            "messages": [{
                "role": "user",
                "content": f"{prompt}\n\nРеши задачу. Ответ должен содержать только решение без пояснений."
            }],
            "temperature": 0.7,
            "max_tokens": 2000
        }

        try:
            response = requests.post(
                self.API_URL,
                json=data,
                headers=headers,
                timeout=30
            )
            
            if response.status_code == 402:
                logging.error("Payment required. Check your API subscription.")
                return None
                
            response.raise_for_status()
            result = response.json()
            self.last_request_time = time.time()
            return result.get('choices', [{}])[0].get('message', {}).get('content', '')
            
        except requests.exceptions.RequestException as e:
            logging.error(f"API Request failed: {e}")
            return None

    @staticmethod
    def human_like_typing(text: str) -> None:
        """Имитация человеческого ввода с ошибками"""
        if not text:
            return

        for char in text:
            try:
                keyboard.press(char)
                keyboard.release(char)
                time.sleep(random.uniform(0.02, 0.2))
                
                # Имитация ошибок с вероятностью 2%
                if random.random() < 0.02:
                    # Стирание 1-3 символов
                    for _ in range(random.randint(1, 3)):
                        keyboard.press(Key.backspace)
                        keyboard.release(Key.backspace)
                        time.sleep(random.uniform(0.1, 0.3))
                    
                    # Повторный ввод с возможными опечатками
                    for c in [char] + [random.choice('abcdefghijklmnopqrstuvwxyz') 
                                     for _ in range(random.randint(0, 2))]:
                        keyboard.press(c)
                        keyboard.release(c)
                        time.sleep(random.uniform(0.05, 0.15))
                        
            except Exception as e:
                logging.error(f"Typing error: {e}")
                continue

    @staticmethod
    def get_clipboard() -> Optional[str]:
        """Безопасное получение текста из буфера обмена"""
        try:
            # Проверка наличия текста в буфере
            text = pyperclip.paste().strip()
            return text if text else None
        except Exception as e:
            logging.error(f"Clipboard error: {e}")
            return None

    def process_task(self) -> None:
        """Основной процесс обработки задачи"""
        logging.info("Hotkey activated, checking clipboard...")
        task = self.get_clipboard()
        
        if not task:
            logging.warning("No text found in clipboard")
            return

        logging.info(f"Task found: {task[:50]}...")  # Логируем начало задачи
        solution = self.send_to_api(task)
        
        if solution:
            logging.info("Received solution, typing...")
            self.human_like_typing(solution)
            logging.info("Typing completed")
        else:
            logging.error("Failed to get solution from API")

def main():
    print("""\nDeepSeek Solver (Ctrl+Alt+S)
----------------------------------
1. Скопируйте задачу в буфер обмена
2. Нажмите Ctrl+Alt+S для решения
3. Убедитесь, что курсор в нужном поле
----------------------------------""")

    # Явно указываем путь к .env файлу
    env_path = os.path.join(os.path.dirname(__file__), '.env')
    if os.path.exists(env_path):
        load_dotenv(env_path)
    else:
        logging.warning(".env file not found, using system environment variables")

    solver = DeepSeekSolver()
    
    from pynput import keyboard as kb
    
    def on_activate():
        solver.process_task()

    # Исправленные комбинации горячих клавиш
    hotkey = kb.GlobalHotKeys({
        '<ctrl>+<alt>+s': on_activate,
        '<ctrl>+<shift>+<space>': on_activate  # Ключевое изменение - добавил <> вокруг space
    })

    try:
        with hotkey:
            logging.info("Service started. Waiting for hotkey...")
            hotkey.join()
    except KeyboardInterrupt:
        logging.info("Service stopped by user")
    except Exception as e:
        logging.critical(f"Fatal error: {e}")
    finally:
        sys.exit(0)

if __name__ == "__main__":
    main()
