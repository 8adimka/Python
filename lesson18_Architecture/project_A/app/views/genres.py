

from flask import request
from flask_restx import Namespace, Resource
from app.database import db
from app.models import Genre, GenreSchema

genres_ns = Namespace('genres')

genres_schema = GenreSchema(many=True)
genre_schema = GenreSchema()

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
        