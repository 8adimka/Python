from flask import Flask
from flask_marshmallow import Marshmallow
from app.database import db

app = Flask (__name__)
ma = Marshmallow(app)

class Genre(db.Model):
    __tablename__ = 'genre'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255))

class GenreSchema (ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Genre
        include_relationship = True
        load_instance = True
