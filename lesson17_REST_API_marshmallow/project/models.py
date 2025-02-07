from flask import Flask, request
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import ForeignKey
from flask_marshmallow import Marshmallow
from sqlalchemy.orm import relationship
from marshmallow import Schema, fields

app = Flask (__name__)

db = SQLAlchemy()
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

class Director(db.Model):
    __tablename__ = 'director'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255))

class Genre(db.Model):
    __tablename__ = 'genre'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255))


class DirectorSchema (ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Director
        include_relationship = True
        load_instance = True

class GenreSchema (ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Genre
        include_relationship = True
        load_instance = True

class MovieSchema (ma.SQLAlchemyAutoSchema):
    director = fields.Nested(DirectorSchema)
    genre = fields.Nested(GenreSchema)
    class Meta:
        model = Movie
        include_relationship = True
        include_fk = True
        load_instance = True
    