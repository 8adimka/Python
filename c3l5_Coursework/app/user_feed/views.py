from flask import Blueprint, request, jsonify, render_template, session, redirect, current_app

from units import (
    get_posts_all,
    get_comments_all,
    get_posts_by_user,
    get_comments_by_post_id,
    search_for_posts,
    get_post_by_pk,
)

usr_feed_blueprint = Blueprint ('usr_feed_blueprint',
                        __name__,
                        template_folder='templates',  # Указываем относительный путь к папке для шаблонов
                        static_folder='static'  # Указываем относительный путь к папке для статических файлов
                        )

@usr_feed_blueprint.route('/users/<username>', methods=['GET', 'POST'])
def usr_feed_page (username):

    posts = get_posts_by_user(username)

    return render_template('user-feed.html', posts=posts)
