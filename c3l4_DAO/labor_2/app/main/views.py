from flask import Blueprint, render_template

main_blueprint = Blueprint('main_blueprint', __name__)

@main_blueprint.route('/')
def page_index():
    return render_template ("main_index.html")
