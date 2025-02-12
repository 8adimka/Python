from flask import request
from app.dao.models.genres import Genre, GenreSchema

#CRUD

genres_schema = GenreSchema(many=True)
genre_schema = GenreSchema()

class GenreDAO:
    def __init__(self, session):
        self.session = session

    def get_one(self,genre_id):
        """GET genre by ID"""
        return self.session.query(Genre).get(genre_id)
    
    def get_all(self):
        """GET all genres"""
        return self.session.query(Genre).all()
    
    def create (self, data):
        """Make new record - genre"""
        new_genre = genre_schema.load(data)
        self.session.add(new_genre)
        self.session.commit()
        return new_genre

    def update (self, genre):
        """PUT genre by ID"""
        self.session.add(genre)
        self.session.commit()
        return genre

    def delete(self, genre_id):
        """Delete genre by ID"""
        genre = self.get_one(genre_id)
        self.session.delete(genre)
        self.session.commit()


