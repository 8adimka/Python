from flask import Blueprint, render_template, request, redirect, session, current_app
import sqlite3

registr_blueprint = Blueprint ('registr_blueprint', __name__,
                               template_folder='templates',  # Указываем папку для шаблонов
                                 static_folder='static'  # Указываем папку для статических файлов
                               )

@registr_blueprint.route ('/registr/', methods=['GET', 'POST'])
def registr_page ():

    PASSWORD_DB_PATH = current_app.config['PASSWORD_DB_PATH']

    username = request.form.get('username', '').lower()
    user_password = request.form.get('password', '')
    result = None

    if username and user_password:
        with sqlite3.connect (PASSWORD_DB_PATH) as con:
            cur = con.cursor()
            cur.execute("INSERT INTO users (name, password) VALUES (?, ?)", (username, user_password))
            cur.execute("""SELECT users.name, users.id FROM users""")
            user_name_list = cur.fetchall()
            for user in user_name_list:
                if user[0] == username:
                    session['user_id'] = user[1]

            result = True
    return render_template('registr.html', result=result)
    