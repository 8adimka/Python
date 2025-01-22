from flask import Flask, session, request_started, render_template, jsonify
import os, sqlite3

from app.feed.views import feed_blueprint
from app.post.views import post_blueprint
from app.search.views import search_blueprint
from app.user_feed.views import usr_feed_blueprint
from app.api.views import api_blueprint


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
# app.register_blueprint (search_blueprint)

# Обработчик ошибки 404
@app.errorhandler(404)
def page_not_found(e):
    # Возвращаем статус 404 и пользовательскую страницу
    return render_template('error_404.html'), 404

# Обработчик ошибки 500
@app.errorhandler(500)
def internal_server_error(e):
    # Возвращаем статус 500 и пользовательскую страницу
    return render_template('error_500.html'), 500


if __name__ == ('__main__'):
    app.run (debug=True)
    # app.run (host='0.0.0.0', port=5000)
