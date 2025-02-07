# from flask import Flask, request, render_template, jsonify, Response
# import json

# app = Flask(__name__)
# app.config['JSON_AS_ASCII'] = False

# movies = [{
#         "title": "Йеллоустоун",
#         "trailer": "https://www.youtube.com/watch?v=UKei_d0cbP4",
#         "year": 2018,
#         "rating": 8.6,
#         "pk": 1
#     }, {
#         "title": "Омерзительная восьмерка",
#         "trailer": "https://www.youtube.com/watch?v=lmB9VWm0okU",
#         "year": 2015,
#         "rating": 7.8,
#         "genre_id": 4,
#         "pk": 2
#     }, {
#         "title": "Вооружен и очень опасен",
#         "trailer": "https://www.youtube.com/watch?v=hLA5631F-jo",
#         "year": 1978,
#         "rating": 6,
#         "pk": 3
#     }
# ]


# @app.route('/', methods=["GET"])
# def page_index():
#     return jsonify(movies)


# @app.route('/<int:movie_id>/')
# def get_movie (movie_id):
#     # return jsonify(movies[movie_id]),200
#     json_data = json.dumps(movies[movie_id], ensure_ascii=False)  # ❗ Преобразуем в строку
#     return Response(json_data, status=200, mimetype="application/json")  # ❗ Указываем заголовок вручную

# app.run()

from flask import Flask, jsonify, request
from flask_restx import Api, Resource
from flask_sqlalchemy import SQLAlchemy
from marshmallow import Schema, fields
from flask_marshmallow import Marshmallow
from sqlalchemy.orm import relationship

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////tmp/test.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['JSON_AS_ASCII'] = False
db = SQLAlchemy(app)
ma = Marshmallow(app)



movies_data = [{
        "title": "Йеллоустоун",
        "trailer": "https://www.youtube.com/watch?v=UKei_d0cbP4",
        "year": 2018,
        "rating": 8.6,
        "id": 1
    }, {
        "title": "Омерзительная восьмерка",
        "trailer": "https://www.youtube.com/watch?v=lmB9VWm0okU",
        "year": 2015,
        "rating": 7.8,
        "id": 2
    }, {
        "title": "Вооружен и очень опасен",
        "trailer": "https://www.youtube.com/watch?v=hLA5631F-jo",
        "year": 1978,
        "rating": 6,
        "id": 3
    }
]


class Movie(db.Model):
    __tablename__ = 'movie'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255))
    trailer = db.Column(db.String(255))
    year = db.Column(db.Integer)
    rating = db.Column(db.Integer)


class MovieSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Movie
        load_instance = True

movie_schema = MovieSchema()
movies_schema = MovieSchema(many=True)


@app.route("/")
def init_page():
    db.drop_all()
    db.create_all()
    movies = [Movie(**movie) for movie in movies_data]
    db.session.add_all(movies)
    db.session.commit()
    return "База данных создана"


@app.route("/movies/")
def get_movies():

    movies_data = Movie.query.all()
    return movies_schema.dump(movies_data), 200


@app.route("/movies/<int:movie_id>")
def get_single_movie(movie_id):
    movie = db.session.query(Movie).get_or_404(movie_id)

    return movie_schema.dump(movie), 200


app.run()