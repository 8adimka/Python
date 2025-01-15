from flask import Flask, render_template
from candidates_dao import CandidatesDAO
from config import Config

candidates_dao = CandidatesDAO()

app = Flask(__name__)
app.config.from_object(Config)
# app.config.from_pyfile('config.py')


@app.route("/")
def page_index():
  candidates = candidates_dao.get_all()
  return render_template("index.html", candidates=candidates)

@app.route("/skills/<skill_name>")
def page_skill(skill_name):
  candidates = candidates_dao.get_by_skill(skill_name)
  return render_template("skill.html", candidates=candidates)

@app.route("/<int:uid>")
def page_candidate(uid):
  candidate = candidates_dao.get_by_id(uid)
  return render_template("candidate.html", candidate=candidate)

app.run()
