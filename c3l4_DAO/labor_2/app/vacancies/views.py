from flask import Blueprint, render_template
from .dao.vacancies_dao import VacanciesDAO

vacancies_blueprint = Blueprint('vacancies_blueprint', __name__, template_folder="templates")

# Создаем DAO для вакансий
vacancies_dao = VacanciesDAO("/home/v/Python/c3l4_DAO/labor_2/data/vacancies.json")


@vacancies_blueprint.route('/vacancies/')
def page_vacancies():
    vacancies = vacancies_dao.get_all()
    return render_template("vacancies_index.html", vacancies=vacancies)


@vacancies_blueprint.route('/vacancies/<int:pk>/')
def page_vacancy(pk):
    vacancy = vacancies_dao.get_by_pk(pk)
    return render_template("vacancies_single.html", vacancy=vacancy)
