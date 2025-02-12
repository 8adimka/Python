from flask import request
from app.dao.models.directors import Director, DirectorSchema

#CRUD

directors_schema = DirectorSchema(many=True)
director_schema = DirectorSchema()

class DirectorDAO:
    def __init__(self, session):
        self.session = session

    def get_one(self,director_id):
        """GET director by ID"""
        return self.session.query(Director).get(director_id)
    
    def get_all(self):
        """GET all directors"""
        return self.session.query(Director).all()
    
    def create (self, data):
        """Make new record - director"""
        new_director = director_schema.load(data)
        self.session.add(new_director)
        self.session.commit()
        return new_director

    def update (self, director):
        """update director by ID"""
        self.session.add(director)
        self.session.commit()
        return director

    def delete(self, director_id):
        """Delete director by ID"""
        director = self.get_one(director_id)
        self.session.delete(director)
        self.session.commit()


