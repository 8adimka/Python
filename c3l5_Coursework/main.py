from flask import Flask, session, request_started, render_template, jsonify, request
import os, sqlite3, logging, datetime

from app.feed.views import feed_blueprint
from app.post.views import post_blueprint
from app.search.views import search_blueprint
from app.user_feed.views import usr_feed_blueprint
from app.api.views import api_blueprint
from app.bookmarks.views import bookmarks_blueprint

# Настройка логирования
LOG_DIR = './c3l5_Coursework/logs'
LOG_FILE = os.path.join(LOG_DIR, 'api.log')
ERROR_LOG_FILE = os.path.join(LOG_DIR, 'errores.log')

# Создаем директорию для логов, если она не существует
os.makedirs(LOG_DIR, exist_ok=True)

# Настройка логгера
logging.basicConfig(
    filename=LOG_FILE,
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] %(message)s'
)
logger = logging.getLogger()
console_handler = logging.StreamHandler() # Создаем обработчик для вывода логов в консоль
logger.addHandler(console_handler) # Добавляем обработчик в логгер

# Создаем обработчик для записи ошибок в файл errores.log
error_file_handler = logging.FileHandler(ERROR_LOG_FILE)
error_file_handler.setLevel(logging.ERROR)  # Уровень ERROR для этого обработчика
logger.addHandler(error_file_handler)


app = Flask (__name__)
app.secret_key = '1111'  # Необходимо для использования сессий

# Динамические пути
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
POSTS_FILE = os.path.join(BASE_DIR, 'static', 'data', 'posts.json')
COMMENTS_FILE = os.path.join(BASE_DIR, 'static', 'data', 'comments.json')

app.config['POSTS_FILE'] = POSTS_FILE
app.config['COMMENTS_FILE'] = COMMENTS_FILE


# Регистрация Blueprints
app.register_blueprint (feed_blueprint)
app.register_blueprint (post_blueprint)
app.register_blueprint (search_blueprint)
app.register_blueprint (usr_feed_blueprint)
app.register_blueprint (api_blueprint)
app.register_blueprint (bookmarks_blueprint)

# Обработчик ошибки 404
@app.errorhandler(404)
def api_not_found(e):
    logger.error(f"Ошибка 404: {request.method} {request.path} от {request.remote_addr}")
    return render_template('error_404.html'), 404

# Обработчик ошибки 500
@app.errorhandler(500)
def api_internal_error(e):
    logger.critical(f"Ошибка 500: {request.method} {request.path} от {request.remote_addr}")
    return render_template('error_500.html'), 500

# Обработчик ошибки 405
@app.errorhandler(405)
def api_method_not_allowed(e):
    logger.error(f"Ошибка 405: {request.method} {request.path} от {request.remote_addr}")
    return render_template('error_404.html'), 405


if __name__ == ('__main__'):
    app.run (debug=True)
    # app.run (host='0.0.0.0', port=5000)
