from flask import request
from app.dao.models.movies import Movie, MovieSchema

#CRUD

movies_schema = MovieSchema(many=True)
movie_schema = MovieSchema()

class MovieDAO:
    def __init__(self, session):
        self.session = session

    def get_one(self,movie_id):
        """GET movie by ID"""
        return self.session.query(Movie).get(movie_id)
    
    def get_all(self):
        """GET all movies"""
        return self.session.query(Movie).all()

    def filter_by(self, **filters):
        """GET filtered movies"""
        return self.session.query(Movie).filter_by(**filters).all()
    
    def create (self, data):
        """Make new record - movie"""
        new_movie = movie_schema.load(data)
        self.session.add(new_movie)
        self.session.commit()
        return new_movie

    def update (self, movie):
        """PUT movie by ID"""
        self.session.add(movie)
        self.session.commit()
        return movie

    def delete(self, movie_id):
        """Delete movie by ID"""
        movie = self.get_one(movie_id)
        self.session.delete(movie)
        self.session.commit()


