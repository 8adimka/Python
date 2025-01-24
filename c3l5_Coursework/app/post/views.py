from flask import Blueprint, request, jsonify, render_template, session, redirect, current_app

from units import (
    get_posts_all,
    get_comments_all,
    get_posts_by_user,
    get_comments_by_post_id,
    search_for_posts,
    get_post_by_pk,
)

post_blueprint = Blueprint ('post_blueprint',
                        __name__,
                        template_folder='templates',  # Указываем относительный путь к папке для шаблонов
                        static_folder='static'  # Указываем относительный путь к папке для статических файлов
                        )

@post_blueprint.route('/post/<int:postid>/', methods=['GET', 'POST'])
def feed_page(postid):

    post = get_post_by_pk(postid)
    comments = get_comments_by_post_id(postid)
    comments_counter = len(comments)

    return render_template('post.html', post=post, comments=comments, comments_counter=comments_counter)
