from marshmallow import fields
from flask import Flask
from flask_marshmallow import Marshmallow
from app.database import db
from app.dao.models.directors import DirectorSchema
from app.dao.models.genres import GenreSchema

app = Flask (__name__)
ma = Marshmallow(app)

class Movie(db.Model):
    __tablename__ = 'movie'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255))
    description = db.Column(db.String(255))
    trailer = db.Column(db.String(255))
    year = db.Column(db.Integer)
    rating = db.Column(db.Integer)
    genre_id = db.Column(db.Integer, db.ForeignKey("genre.id"))
    genre = db.relationship("Genre")
    director_id = db.Column(db.Integer, db.ForeignKey("director.id"))
    director = db.relationship("Director")

class MovieSchema (ma.SQLAlchemyAutoSchema):
    director = fields.Nested(DirectorSchema)
    genre = fields.Nested(GenreSchema)
    class Meta:
        model = Movie
        include_relationship = True
        include_fk = True
        load_instance = True
