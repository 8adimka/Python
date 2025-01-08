from flask import Blueprint, render_template

enter_blueprint = Blueprint ('enter_blueprint', __name__,
                             template_folder='templates',
                             static_folder='static')

@enter_blueprint.route ('/enter/')
def reg_page(): 
    return render_template('enter.html')
