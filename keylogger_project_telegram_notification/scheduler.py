import time
import threading
from sender import send_log
from config import TIME_OUT

SEND_INTERVAL = TIME_OUT  # время ожидания перед отправкой

def send_logs_periodically():
    while True:
        send_log()
        time.sleep(SEND_INTERVAL)

def run_scheduler():
    thread = threading.Thread(target=send_logs_periodically, daemon=True)
    thread.start()
    