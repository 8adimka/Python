
from flask import request
from flask_restx import Namespace, Resource
from app.database import db
from app.models import Director, DirectorSchema

directors_ns = Namespace('directors')

directors_schema = DirectorSchema(many=True)
director_schema = DirectorSchema()

@directors_ns.route ('/')
class directorsView(Resource):
    def get (self):
        all_directors = db.session.query(Director).all()
        return directors_schema.dump(all_directors), 200
    
    def post(self):
        try:
            data_json = request.json
            new_director = director_schema.load(data_json)
            db.session.add(new_director)
            db.session.commit()
            return director_schema.dump(new_director), 201
    
        except Exception as e:
            return f'Error {e}', 404
 