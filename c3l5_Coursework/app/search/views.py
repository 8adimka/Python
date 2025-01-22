from flask import Blueprint, request, jsonify, render_template, session, redirect, current_app

from units import (
    get_posts_all,
    get_comments_all,
    get_posts_by_user,
    get_comments_by_post_id,
    search_for_posts,
    get_post_by_pk,
)

search_blueprint = Blueprint ('search_blueprint',
                        __name__,
                        template_folder='templates',  # Указываем относительный путь к папке для шаблонов
                        static_folder='static'  # Указываем относительный путь к папке для статических файлов
                        )

@search_blueprint.route('/search/', methods=['GET', 'POST'])
def feed_page():

    s = request.form.get('search')

    posts = search_for_posts(s)
    posts_count = len(posts)

    return render_template('search.html', posts_count=posts_count, posts=posts)