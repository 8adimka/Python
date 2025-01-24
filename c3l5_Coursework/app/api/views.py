# from flask import Blueprint, request, jsonify, render_template, session, redirect, current_app

# from units import (
#     get_posts_all,
#     get_comments_all,
#     get_posts_by_user,
#     get_comments_by_post_id,
#     search_for_posts,
#     get_post_by_pk,
# )

# api_blueprint = Blueprint('api_blueprint', __name__)

# # Эндпоинт для получения всех постов
# @api_blueprint.route('/api/posts', methods=['GET'])
# def get_all_posts():
#     posts_class = get_posts_all()  # эта функция возвращает список постов в виде объектов класса Post
#     posts = [
#         {'poster_name': post.poster_name,
#          'poster_avatar': post.poster_avatar,
#          'pic': post.pic, 'content': post.content,
#          'views_count':post.views_count,
#          'likes_count':post.likes_count,
#          'pk': post.pk} for post in posts_class]
#     return jsonify(posts), 200

# # Эндпоинт для получения одного поста по ID
# @api_blueprint.route('/api/posts/<int:post_id>', methods=['GET'])
# def get_post(post_id):
#     post_class = get_post_by_pk(post_id)  # эта функция возвращает пост в виде объекта класса Post
#     post = {'poster_name': post_class.poster_name,
#          'poster_avatar': post_class.poster_avatar,
#          'pic': post_class.pic, 'content': post_class.content,
#          'views_count':post_class.views_count,
#          'likes_count':post_class.likes_count,
#          'pk': post_class.pk}

#     if not post:
#         return jsonify({'error': 'Post not found'}), 404
#     return jsonify(post), 200

# @api_blueprint.errorhandler(404)
# def api_not_found(e):
#     return jsonify({f'error - {e}': 'Resource not found'}), 404
 
import os, logging
from flask import Blueprint, request, jsonify, render_template, session, redirect, current_app

from units import (
    get_posts_all,
    get_comments_all,
    get_posts_by_user,
    get_comments_by_post_id,
    search_for_posts,
    get_post_by_pk,
)

api_blueprint = Blueprint('api_blueprint', __name__)

logger = logging.getLogger(__name__)

# Эндпоинт для получения всех постов
@api_blueprint.route('/api/posts/', methods=['GET'])
def get_all_posts():
    logger.info(f"Запрос {request.method} {request.path} от {request.remote_addr}")
    posts_class = get_posts_all()  # Функция возвращает список объектов класса Post
    posts = [
        {
            'poster_name': post.poster_name,
            'poster_avatar': post.poster_avatar,
            'pic': post.pic,
            'content': post.content,
            'views_count': post.views_count,
            'likes_count': post.likes_count,
            'pk': post.pk,
            'hashtags': post.hashtags}
        for post in posts_class]
    return jsonify(posts), 200

# Эндпоинт для получения одного поста по ID
@api_blueprint.route('/api/posts/<int:post_id>', methods=['GET'])
def get_post(post_id):
    logger.info(f"Запрос {request.method} {request.path} от {request.remote_addr}")
    post_class = get_post_by_pk(post_id)  # Функция возвращает объект класса Post
    if not post_class:
        logger.warning(f"Пост с id={post_id} не найден")
        return jsonify({'error': 'Post not found'}), 404

    post = {
        'poster_name': post_class.poster_name,
        'poster_avatar': post_class.poster_avatar,
        'pic': post_class.pic,
        'content': post_class.content,
        'views_count': post_class.views_count,
        'likes_count': post_class.likes_count,
        'pk': post_class.pk,
        'hashtags': post_class.hashtags
    }
    return jsonify(post), 200
