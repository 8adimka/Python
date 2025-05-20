import time
import random
import os
import pyperclip
import requests
import re
from typing import Optional
from pynput.keyboard import Controller, Key
from pynput import keyboard as kb
from Xlib import X, display
import signal
import sys
from dotenv import load_dotenv
import tenacity

def signal_handler(sig, frame):
    print("\nПрограмма завершает работу.")
    sys.exit(0)

class DaemonContext:
    def __init__(self, detach_process=True, umask=0o022, working_directory='/'):
        self.detach = detach_process
        self.umask = umask
        self.workdir = working_directory
        
    def __enter__(self):
        if self.detach:
            self._daemonize()
        os.chdir(self.workdir)
        os.umask(self.umask)
        return self
        
    def __exit__(self, *args):
        pass
        
    def _daemonize(self):
        try:
            if os.fork() > 0:
                sys.exit(0)
        except OSError as e:
            sys.stderr.write(f"Fork #1 failed: {e}\n")
            sys.exit(1)
            
        os.setsid()
        os.umask(0)
        
        try:
            if os.fork() > 0:
                sys.exit(0)
        except OSError as e:
            sys.stderr.write(f"Fork #2 failed: {e}\n")
            sys.exit(1)
            
        sys.stdout.flush()
        sys.stderr.flush()
        
        si = open(os.devnull, 'r')
        so = open(os.devnull, 'a+')
        se = open(os.devnull, 'a+')
        
        os.dup2(si.fileno(), sys.stdin.fileno())
        os.dup2(so.fileno(), sys.stdout.fileno())
        os.dup2(se.fileno(), sys.stderr.fileno())

class CodePreprocessor:
    @staticmethod
    def clean_code(code: str) -> str:
        """Очищает код от лишних отступов и форматирования"""
        # Удаляем все лишние отступы и пустые строки
        lines = [line.rstrip() for line in code.split('\n') if line.strip()]
        
        # Нормализуем отступы
        min_indent = float('inf')
        for line in lines:
            if line.strip():
                indent = len(line) - len(line.lstrip())
                min_indent = min(min_indent, indent)
        
        # Удаляем минимальный отступ у всех строк
        if min_indent != float('inf'):
            lines = [line[min_indent:] if line.strip() else line for line in lines]
        
        return '\n'.join(lines)

    @staticmethod
    def fix_common_typos(code: str) -> str:
        """Исправляет распространенные опечатки"""
        corrections = {
            'Optionaal': 'Optional',
            'nnode': 'node',
            'leftt_max': 'left_max',
            'rigght_max': 'right_max',
            'maax_sum': 'max_sum',
            'hellper': 'helper',
            'caandy': 'candy',
            'raatings': 'ratings',
            'rattings': 'ratings',
            'canddies': 'candies',
            'cannddies': 'candies',
            'foor': 'for',
            'ratinggss': 'ratings',
            'ratinngs': 'ratings',
            'mmax': 'max',
            'canndies': 'candies'
        }
        
        for wrong, correct in corrections.items():
            code = code.replace(wrong, correct)
            
        return code

class DeepSeekSolver:
    def __init__(self):
        self.API_URL = "https://api.deepseek.com/v1/chat/completions"
        self.API_KEY = self._get_api_key()
        self.last_request_time = 0
        self.RATE_LIMIT_DELAY = 3
        self.keyboard = Controller()
        self.dpy = display.Display()
        self.processing_task = False
        self.paused = False
        self.current_typing_task = None
        self.preprocessor = CodePreprocessor()
        self.current_indent = 0
        self.prev_line_ended_with_colon = False

    def _get_api_key(self) -> str:
        load_dotenv()
        api_key = os.getenv("DEEPSEEK_API_KEY")
        if not api_key:
            raise RuntimeError("API ключ не найден в файле .env")
        return api_key

    @tenacity.retry(wait=tenacity.wait_exponential(multiplier=1, min=4, max=10))
    def send_to_api(self, prompt: str) -> Optional[str]:
        current_time = time.time()
        if current_time - self.last_request_time < self.RATE_LIMIT_DELAY:
            time.sleep(self.RATE_LIMIT_DELAY - (current_time - self.last_request_time))

        headers = {"Authorization": f"Bearer {self.API_KEY}", "Content-Type": "application/json"}
        data = {
            "model": "deepseek-chat",
            "messages": [{
                "role": "user",
                "content": f"{prompt}\n\nProvide only the correct Python code solution without any comments, explanations or additional text. The code must be perfectly formatted with proper indentation (without extra spaces) and no typos. Return only the code."
            }],
            "temperature": 0.2,
            "max_tokens": 2000
        }

        try:
            response = requests.post(self.API_URL, json=data, headers=headers, timeout=30)
            response.raise_for_status()
            self.last_request_time = time.time()
            code = response.json()['choices'][0]['message']['content']
            
            # Удаляем markdown formatting если есть
            code = code.replace('```python', '').replace('```', '').strip()
            return code
        except requests.exceptions.RequestException as e:
            print(f"Ошибка API запроса: {e}")
            return None

    def human_like_typing(self, text: str) -> None:
        if not text or self.processing_task:
            return

        self.processing_task = True
        self.current_typing_task = text
        self.current_indent = 0
        self.prev_line_ended_with_colon = False
        
        try:
            # Активируем окно
            window = self.dpy.get_input_focus().focus
            if window:
                window.set_input_focus(X.RevertToParent, X.CurrentTime)
                self.dpy.flush()

            time.sleep(0.5 + random.random() * 0.3)

            # Очищаем и проверяем код перед вводом
            clean_code = self.preprocessor.clean_code(text)
            clean_code = self.preprocessor.fix_common_typos(clean_code)
            
            # Разбиваем на строки
            lines = clean_code.split('\n')
            
            for line in lines:
                if self.paused:
                    while self.paused:
                        time.sleep(0.1)
                        continue

                # Определяем текущий отступ
                stripped_line = line.lstrip()
                line_indent = len(line) - len(stripped_line)
                
                # Если предыдущая строка заканчивалась двоеточием, IDE уже добавила отступ
                if self.prev_line_ended_with_colon:
                    # Нажимаем backspace если AI добавил лишние отступы
                    while self.current_indent > line_indent:
                        self.keyboard.press(Key.backspace)
                        self.keyboard.release(Key.backspace)
                        self.current_indent -= 4
                        time.sleep(0.05)
                else:
                    # Добавляем отступы если нужно
                    while self.current_indent < line_indent:
                        self.keyboard.press(Key.space)
                        self.keyboard.release(Key.space)
                        self.current_indent += 1
                        time.sleep(0.05)
                
                # Вводим строку
                self._type_line(stripped_line)
                
                # Перенос строки
                self.keyboard.press(Key.enter)
                self.keyboard.release(Key.enter)
                time.sleep(random.uniform(0.2, 0.3))
                
                # Обновляем состояние для следующей строки
                self.prev_line_ended_with_colon = line.rstrip().endswith(':')
                if self.prev_line_ended_with_colon:
                    self.current_indent += 4
                elif stripped_line.startswith('return'):
                    self.current_indent = max(0, self.current_indent - 4)

        except Exception as e:
            print(f"Ошибка во время имитации ввода: {e}")
        finally:
            self.processing_task = False
            self.current_typing_task = None
            self.current_indent = 0
            self.prev_line_ended_with_colon = False

    def _type_line(self, line: str) -> None:
        """Вводит одну строку кода с человеко-подобными ошибками"""
        # Пауза перед началом ввода строки
        time.sleep(random.uniform(0.1, 0.2))
        
        for char in line:
            if self.paused:
                while self.paused:
                    time.sleep(0.1)
                    continue
            
            # Базовая задержка
            delay = random.uniform(0.05, 0.12)
            time.sleep(delay)
            
            # Ввод символа
            self.keyboard.press(char)
            self.keyboard.release(char)
            
            # Редкие ошибки (2% chance)
            if random.random() < 0.02 and char.isalpha():
                time.sleep(0.1)
                # Вводим неправильный символ
                wrong_char = chr(ord(char) + random.randint(-1, 1))
                self.keyboard.press(wrong_char)
                self.keyboard.release(wrong_char)
                time.sleep(0.1)
                
                # Исправляем
                self.keyboard.press(Key.backspace)
                self.keyboard.release(Key.backspace)
                time.sleep(0.1)
                
                # Вводим правильный символ
                self.keyboard.press(char)
                self.keyboard.release(char)
                time.sleep(0.1)

    def toggle_pause(self) -> None:
        self.paused = not self.paused
        status = "приостановлен" if self.paused else "возобновлен"
        print(f"Ввод {status}")

    def process_task(self) -> None:
        try:
            if self.processing_task:
                print("Предыдущая задача仍在处理中...")
                return

            task = pyperclip.paste().strip()
            if not task:
                print("Клипборд пуст.")
                return

            solution = self.send_to_api(task)
            if solution:
                print("Получено решение от API")
                clean_solution = solution.replace('```python', '').replace('```', '').strip()
                self.human_like_typing(clean_solution)
            else:
                print("Не удалось получить решение от API.")

        except Exception as e:
            print(f"Ошибка при обработке задачи: {e}")

def run_daemon():
    solver = DeepSeekSolver()

    def on_activate():
        solver.process_task()

    def on_pause():
        solver.toggle_pause()

    hotkeys = kb.GlobalHotKeys({
        '<ctrl>+<alt>+s': on_activate,
        '<ctrl>+<shift>+p': on_pause
    })
    
    print("Программа запущена и готова к работе!")
    print("Используйте Ctrl+Alt+S для активации решения.")
    print("Используйте Ctrl+Shift+P для паузы/возобновления ввода.")
    
    with hotkeys:
        try:
            hotkeys.join()
        except:
            pass

if __name__ == "__main__":
    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)
    
    try:
        solver = DeepSeekSolver()
    except RuntimeError as e:
        print(e)
        sys.exit(1)
        
    with DaemonContext(
        detach_process=True,
        umask=0o022,
        working_directory=os.path.expanduser('~')
    ):
        run_daemon()
        