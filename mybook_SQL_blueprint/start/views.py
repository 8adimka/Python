from flask import Blueprint, render_template

start_blueprint = Blueprint(
    'start_blueprint', 
    __name__, 
    template_folder='templates',  # Указываем папку для шаблонов
    static_folder='static'  # Указываем папку для статических файлов
)

@start_blueprint.route('/')
def start_page ():
    return render_template('start.html')
