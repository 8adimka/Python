from flask import Blueprint, render_template
from .dao.candidates_dao import CandidateDAO

# Создаем блупринт
candidates_blueprint = Blueprint('candidates_blueprint', __name__, template_folder="templates")

# Создаем DAO
candidates_dao = CandidateDAO("/home/v/Python/c3l4_DAO/labor_2/data/candidates.json")

# Создаем вьюшку для кандидатов
@candidates_blueprint.route('/candidates/')
def page_candidates():
    candidates = candidates_dao.get_all()
    return render_template("candidates_index.html", candidates=candidates)

# Создаем вьюшку для одного кандидата
@candidates_blueprint.route('/candidates/<int:pk>/')
def page_candidate_all(pk):
    candidate = candidates_dao.get_by_pk(pk)
    return render_template("candidates_single.html", candidate=candidate)
