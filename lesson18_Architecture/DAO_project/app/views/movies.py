from app.container import movie_service
from flask import request
from flask_restx import Namespace, Resource
from app.database import db
from app.dao.models.movies import Movie, MovieSchema

movies_ns = Namespace('movies')

movies_schema = MovieSchema(many=True)
movie_schema = MovieSchema()

@movies_ns.route ('/')
class MoviesView(Resource):
    def get (self):
        """GET all movies"""
        director_id = request.args.get('director_id')
        genre_id = request.args.get('genre_id')
        all_movies = movie_service.get_all(director_id,genre_id)
        return movies_schema.dump(all_movies), 200
    
    def post(self):
        """Make new record - movie"""
        try:
            data_json = request.json
            new_movie = movie_service.create(data_json)
            return movie_schema.dump(new_movie), 201
    
        except Exception as e:
            return f'Error {e}', 404
        

@movies_ns.route ('/<int:movie_id>')
class MovieView(Resource):
    def get (self, movie_id):
        """GET movie by ID"""
        movie = movie_service.get_one(movie_id)
        return movie_schema.dump(movie), 200
    
    def put(self, movie_id):
        """PUT movie by ID"""
        data_json = request.json
        data_json['id']=movie_id

        movie = movie_service.update(data_json)

        return movie_schema.dump(movie), 200
    
    def patch(self, movie_id):
        """PATCH movie by ID"""
        data_json = request.json
        data_json['id']=movie_id

        movie = movie_service.update_partial(data_json)

        return movie_schema.dump(movie), 204

    def delete(self, movie_id):
        """Delete movie by ID"""
        movie_service.delete(movie_id)
        return {"message": "фильм удален"}, 204
