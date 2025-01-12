from flask import Blueprint, render_template, redirect, request, session, current_app
import sqlite3

login_blueprint = Blueprint ('login_blueprint', __name__,
                             template_folder='templates',  # Указываем папку для шаблонов
                             static_folder='static'  # Указываем папку для статических файлов
                             )

@login_blueprint.route('/login/', methods=['GET'])
def user_login_page():
    return render_template('login.html')


@login_blueprint.route('/login/fail/', methods=['GET'])
def user_login_true():
    return render_template('login_fail.html')


@login_blueprint.route('/login/success/', methods=['GET'])
def user_login_fail():
    return render_template('login_success.html')


@login_blueprint.route('/login/submit/', methods=['POST'])
def user_login_handler():

    PASSWORD_DB_PATH = current_app.config['PASSWORD_DB_PATH'] # Путь к базе данных

    username = request.form.get('username', '').lower()
    password = request.form.get('password', '')
    result = None

    if username and password:
        with sqlite3.connect (PASSWORD_DB_PATH) as con:
            cur = con.cursor()
            cur.execute("""SELECT * FROM users""")
            user_list = cur.fetchall()
            for user in user_list:
                if user[1] == username and user[2] == password:
                    session['user_id'] = user[0] # Записываем id пользователя в сессию
                    result = True
                else:
                    result = False
    if result == True: 
        return redirect('/login/success/', code=302)
    else: 
        return redirect('/login/fail/', code=302)
