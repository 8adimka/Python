# project/
# │── app.py                Основной файл с эндпоинтами
# │── models.py             Определение моделей SQLAlchemy
# │── create_database.py    Настройка БД и заполнение данными
# │── config.py             Конфигурация Flask
# │── __init__.py           Чтобы Python видел папку как модуль

from flask import Flask, request
from flask_restx import Api, Resource
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import ForeignKey
from models import db, Movie, Director, Genre, DirectorSchema, GenreSchema, MovieSchema
from config import Config
from create_database import init_db

app = Flask(__name__)
app.config.from_object(Config)
db.init_app(app)

api = Api(app)

movies_ns = api.namespace('movies')
directors_ns = api.namespace('directors')
genres_ns = api.namespace('genres')

movies_schema = MovieSchema(many=True)
movie_schema = MovieSchema()

directors_schema = DirectorSchema(many=True)
director_schema = DirectorSchema()

genres_schema = GenreSchema(many=True)
genre_schema = GenreSchema()


init_db(app)

@movies_ns.route ('/')
class moviesView(Resource):
    def get (self):
        director_id = request.args.get('director_id')
        genre_id = request.args.get('genre_id')
        if director_id:
            director_movies = db.session.query(Movie).filter(Movie.director_id==director_id).all()
            return movies_schema.dump(director_movies), 200
        elif genre_id:
            genre_movies = db.session.query(Movie).filter(Movie.genre_id==genre_id).all()
            return movies_schema.dump(genre_movies), 200
        all_movies = db.session.query(Movie).all()
        return movies_schema.dump(all_movies), 200
    
    def post(self):
        try:
            data_json = request.json
            new_movie = movie_schema.load(data_json)
            db.session.add(new_movie)
            db.session.commit()
            return movie_schema.dump(new_movie), 201
    
        except Exception as e:
            return f'Error {e}', 404
        

@movies_ns.route ('/<int:movie_id>')
class movieView(Resource):
    def get (self, movie_id):
        movie = Movie.query.get_or_404(movie_id)
        return movie_schema.dump(movie), 200
    
    def put(self, movie_id):
        movie = db.session.query(Movie).get(movie_id)
        data_json = request.json

        movie.title = data_json.get("title")
        movie.description = data_json.get("description")
        movie.trailer = data_json.get("trailer")
        movie.year = data_json.get("year")
        movie.rating = data_json.get("rating")

        db.session.add(movie)
        db.session.commit()

        return movie_schema.dump(movie), 200
    
    def patch(self, movie_id):
        movie = db.session.query(Movie).get(movie_id)
        data_json = request.json

        if "title" in data_json:
            movie.title = data_json.get("title")
        if "description" in data_json:
            movie.description = data_json.get("description")
        if "trailer" in data_json:
            movie.trailer = data_json.get("trailer")
        if "year" in data_json:
            movie.year = data_json.get("year")
        if "rating" in data_json:
            movie.rating = data_json.get("rating")

        db.session.add(movie)
        db.session.commit()

        return movie_schema.dump(movie), 204

    def delete(self, movie_id):
        """Удалить фильм по ID"""
        movie = Movie.query.get_or_404(movie_id)
        db.session.delete(movie)
        db.session.commit()
        return {"message": "фильм удален"}, 204

@directors_ns.route ('/')
class moviesView(Resource):
    def get (self):
        all_movies = db.session.query(Movie).all()
        return movies_schema.dump(all_movies), 200
    
    def post(self):
        try:
            data_json = request.json
            new_movie = movie_schema.load(data_json)
            db.session.add(new_movie)
            db.session.commit()
            return movie_schema.dump(new_movie), 201
    
        except Exception as e:
            return f'Error {e}', 404
        
@genres_ns.route ('/')
class genresView(Resource):
    def get (self):
        all_genres = db.session.query(Genre).all()
        return genres_schema.dump(all_genres), 200
    
    def post(self):
        try:
            data_json = request.json
            new_genre = genre_schema.load(data_json)
            db.session.add(new_genre)
            db.session.commit()
            return genre_schema.dump(new_genre), 201
    
        except Exception as e:
            return f'Error {e}', 404

if __name__ == '__main__':
    app.run(debug=True)
