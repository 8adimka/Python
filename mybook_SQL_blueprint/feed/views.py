from flask import Blueprint, render_template, redirect, session, request, current_app
import sqlite3

feed_blueprint = Blueprint ('feed_blueprint',
                        __name__,
                        template_folder='./templates',  # Указываем относительный путь к папке для шаблонов
                        static_folder='./static'  # Указываем относительный путь к папке для статических файлов
                        )

@feed_blueprint.route('/feed/', methods=['GET', 'POST'])
def feed_page():

    PASSWORD_DB_PATH = current_app.config['PASSWORD_DB_PATH'] # Получаем путь к базе данных из сессии

    user_id = session.get('user_id')

    if user_id:
        with sqlite3.connect (PASSWORD_DB_PATH) as con:
            cur = con.cursor()
            cur.execute("""SELECT users.name, description, image
                        FROM posts
                        JOIN users ON users.id = posts.user_id""")
            publications = cur.fetchall()
        if not publications:
            publications = []
        return render_template('feed_SQL.html', publications=publications)
    else:
        return redirect('/')
