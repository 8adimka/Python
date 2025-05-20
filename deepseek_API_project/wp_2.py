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
        except OSError:
            sys.exit(1)

        os.setsid()
        os.umask(0)

        try:
            if os.fork() > 0:
                sys.exit(0)
        except OSError:
            sys.exit(1)

        sys.stdout.flush()
        sys.stderr.flush()

        with open(os.devnull, 'r') as si, open(os.devnull, 'a+') as so, open(os.devnull, 'a+') as se:
            os.dup2(si.fileno(), sys.stdin.fileno())
            os.dup2(so.fileno(), sys.stdout.fileno())
            os.dup2(se.fileno(), sys.stderr.fileno())

class CodePreprocessor:
    @staticmethod
    def clean_code(code: str) -> str:
        lines = [line.rstrip() for line in code.split('\n') if line.strip()]
        min_indent = min((len(line) - len(line.lstrip()) for line in lines if line.strip()), default=0)
        return '\n'.join([line[min_indent:] for line in lines])

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

    def _wait_if_paused(self):
        while self.paused:
            time.sleep(0.1)

    def toggle_pause(self) -> None:
        self.paused = not self.paused

    def _get_api_key(self) -> str:
        load_dotenv()
        api_key = os.getenv("DEEPSEEK_API_KEY")
        if not api_key:
            raise RuntimeError("API ключ не найден")
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
            return code.replace('```python', '').replace('```', '').strip()
        except requests.exceptions.RequestException:
            return None

    def human_like_typing(self, text: str) -> None:
        if not text or self.processing_task:
            return

        self.processing_task = True
        self.current_typing_task = text
        self.current_indent = 0
        self.prev_line_ended_with_colon = False

        try:
            window = self.dpy.get_input_focus().focus
            if window:
                window.set_input_focus(X.RevertToParent, X.CurrentTime)
                self.dpy.flush()

            clean_code = self.preprocessor.clean_code(text)
            lines = clean_code.split('\n')

            for line in lines:
                self._wait_if_paused()

                stripped_line = line.lstrip()
                line_indent = len(line) - len(stripped_line)

                if self.prev_line_ended_with_colon:
                    while self.current_indent > line_indent:
                        self._wait_if_paused()
                        self.keyboard.press(Key.backspace)
                        self.keyboard.release(Key.backspace)
                        self.current_indent -= 4
                        time.sleep(0.05)
                else:
                    while self.current_indent < line_indent:
                        self._wait_if_paused()
                        self.keyboard.press(Key.space)
                        self.keyboard.release(Key.space)
                        self.current_indent += 1
                        time.sleep(0.05)

                self._type_line(stripped_line)

                self.keyboard.press(Key.enter)
                self.keyboard.release(Key.enter)
                time.sleep(random.uniform(0.3, 0.7))

                self.prev_line_ended_with_colon = line.rstrip().endswith(':')
                if self.prev_line_ended_with_colon:
                    self.current_indent += 4
                elif stripped_line.startswith('return'):
                    self.current_indent = max(0, self.current_indent - 4)

        finally:
            self.processing_task = False
            self.current_typing_task = None
            self.current_indent = 0
            self.prev_line_ended_with_colon = False

    def _type_line(self, line: str) -> None:
        time.sleep(random.uniform(0.1, 0.2))
        word_buffer = ''

        for char in line:
            self._wait_if_paused()

            word_buffer += char

            if char.isspace():
                if len(word_buffer.strip()) > 3 and random.random() < 0.3:
                    time.sleep(random.uniform(0.4, 0.8))
                word_buffer = ''

            delay = random.gauss(0.08, 0.03)
            delay = min(max(0.04, delay), 0.15)
            time.sleep(delay)

            self.keyboard.press(char)
            self.keyboard.release(char)

            if random.random() < 0.02 and char.isalpha():
                wrong_char = chr(ord(char) + random.randint(-1, 1))
                self.keyboard.press(wrong_char)
                self.keyboard.release(wrong_char)
                time.sleep(0.1)
                self.keyboard.press(Key.backspace)
                self.keyboard.release(Key.backspace)
                time.sleep(0.1)
                self.keyboard.press(char)
                self.keyboard.release(char)
                time.sleep(0.1)

    def process_task(self) -> None:
        if self.processing_task:
            return

        task = pyperclip.paste().strip()
        if not task:
            return

        solution = self.send_to_api(task)
        if solution:
            self.human_like_typing(solution)


def run_daemon():
    solver = DeepSeekSolver()

    def on_activate():
        solver.process_task()

    def on_pause():
        solver.toggle_pause()

    hotkeys = kb.GlobalHotKeys({
        '<ctrl>+<alt>+.': on_activate,
        '<ctrl>+<alt>+,': on_pause
    })

    with hotkeys:
        hotkeys.join()

if __name__ == "__main__":
    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)

    try:
        with DaemonContext(
            detach_process=True,
            umask=0o022,
            working_directory=os.path.expanduser('~')
        ):
            run_daemon()
    except RuntimeError:
        sys.exit(1)
