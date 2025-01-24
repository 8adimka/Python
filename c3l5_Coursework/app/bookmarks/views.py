from flask import Blueprint, request, jsonify, render_template, session, redirect, current_app

from units import (
    load_bookmarks,
    save_bookmarks,
    delete_bookmark,
    get_bookmarks_by_post_id,
    search_for_posts,
    get_post_by_pk,
)

bookmarks_blueprint = Blueprint ('bookmarks_blueprint',
                        __name__,
                        template_folder='templates',  # Указываем относительный путь к папке для шаблонов
                        static_folder='static'  # Указываем относительный путь к папке для статических файлов
                        )

@bookmarks_blueprint.route('/toggle_bookmark/', methods=['GET', 'POST'])
def toggle_bookmark():
    post_id = int(request.form.get("post_id"))  # ID поста
    post_class = get_post_by_pk(post_id)
    post = {
            'poster_name': post_class.poster_name,
            'poster_avatar': post_class.poster_avatar,
            'pic': post_class.pic,
            'content': post_class.content,
            'views_count': post_class.views_count,
            'likes_count': post_class.likes_count,
            'pk': post_class.pk,
            'hashtags': post_class.hashtags}
    bookmarks = load_bookmarks()

    # Добавляем или удаляем пост из закладок
    for bookmark in bookmarks:
        if bookmark['pk'] == post_id:
            bookmarks.remove(post)
            save_bookmarks(bookmarks)  # Сохраняем изменения
            return redirect(request.referrer)

    bookmarks.append(post)
    save_bookmarks(bookmarks)  # Сохраняем изменения
    return redirect(request.referrer)

@bookmarks_blueprint.route('/bookmarks/', methods=['GET', 'POST'])
def bookmark():
    post = load_bookmarks()

    return render_template('user-feed.html', posts=post)

