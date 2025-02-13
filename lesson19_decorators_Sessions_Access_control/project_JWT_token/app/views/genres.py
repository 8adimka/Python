
from app.container import genre_service
from flask import request
from flask_restx import Namespace, Resource
from app.database import db
from app.dao.models.genres import GenreSchema

genres_ns = Namespace('genres')

genres_schema = GenreSchema(many=True)
genre_schema = GenreSchema()

@genres_ns.route ('/')
class GenresView(Resource):
    def get (self):
        """GET all genres"""
        all_genres = genre_service.get_all()
        return genres_schema.dump(all_genres), 200
    
    def post(self):
        """Make new record - genre"""
        try:
            data_json = request.json
            new_genre = genre_service.create(data_json)
            return genre_schema.dump(new_genre), 201
    
        except Exception as e:
            return f'Error {e}', 404
        
@genres_ns.route ('/<int:genre_id>')
class GenreView(Resource):
    def get (self, genre_id):
        """GET genre by ID"""
        genre = genre_service.get_one(genre_id)
        return genre_schema.dump(genre), 200
    
    def delete(self, genre_id):
        """Delete genre by ID"""
        genre_service.delete(genre_id)
        return {"message": "жанр удален"}, 204
        