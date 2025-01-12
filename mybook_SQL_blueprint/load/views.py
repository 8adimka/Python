from flask import Blueprint, render_template, redirect, request, url_for, session, current_app
import sqlite3, os

load_blueprint = Blueprint ('load_blueprint',
                            __name__,
                            template_folder='templates',  # Указываем папку для шаблонов
                            static_folder='static'  # Указываем папку для статических файлов
                            )

@load_blueprint.route('/load/', methods=['GET', 'POST'])
def load_page():

    PASSWORD_DB_PATH = current_app.config['PASSWORD_DB_PATH'] # Получаем путь к базе данных из сессии

    user_id = session.get('user_id')  # Получаем user_id из сессии

    if user_id:
        if request.method == 'POST':
            descript = request.form.get('description', '')  # Получить описание
            file = request.files.get('file')  # Получить файл изображения

            if file:
                # Сохраняем файл и публикацию
                filename = file.filename
                filepath = os.path.join(current_app.config['UPLOAD_FOLDER'], filename)
                file.save(filepath)

                with sqlite3.connect (PASSWORD_DB_PATH) as con:
                    cur = con.cursor()
                    cur.execute(
                        "INSERT INTO posts (user_id, description, image) VALUES (?, ?, ?)",
                        (user_id, descript, filename)
                    )

            return redirect(url_for('feed_blueprint.feed_page'))
        return render_template('load_SQL.html')
    else:
        return redirect('/')
