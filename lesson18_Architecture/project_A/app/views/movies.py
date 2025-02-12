
from flask import request
from flask_restx import Namespace, Resource
from app.database import db
from app.models import Movie, MovieSchema

movies_ns = Namespace('movies')

movies_schema = MovieSchema(many=True)
movie_schema = MovieSchema()

@movies_ns.route ('/')
class moviesView(Resource):
    def get (self):
        director_id = request.args.get('director_id')
        genre_id = request.args.get('genre_id')
        if director_id and genre_id:
            dir_gen_movie = Movie.query.filter(Movie.director_id==director_id, Movie.genre_id==genre_id).all()
            return movies_schema.dump(dir_gen_movie), 200
        elif director_id:
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
