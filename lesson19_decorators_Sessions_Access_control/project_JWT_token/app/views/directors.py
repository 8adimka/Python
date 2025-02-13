from app.container import director_service
from flask import request
from flask_restx import Namespace, Resource
from app.database import db
from app.dao.models.directors import Director, DirectorSchema

directors_ns = Namespace('directors')

directors_schema = DirectorSchema(many=True)
director_schema = DirectorSchema()

@directors_ns.route ('/')
class DirectorsView(Resource):
    def get (self):
        """GET all directors"""
        all_directors = director_service.get_all()
        return directors_schema.dump(all_directors), 200
    
    def post(self):
        """Make new record - director"""
        try:
            data_json = request.json
            new_director = director_service.create(data_json)
            return director_schema.dump(new_director), 201
    
        except Exception as e:
            return f'Error {e}', 404

@directors_ns.route ('/<int:director_id>')
class DirectorView(Resource):
    def get (self, director_id):
        """GET director by ID"""
        director = director_service.get_one(director_id)
        return director_schema.dump(director), 200
    
    def delete(self, director_id):
        """Delete director by ID"""
        director_service.delete(director_id)
        return {"message": "режисёр удален"}, 204
 