from flask import Flask
from flask_marshmallow import Marshmallow
from app.database import db

app = Flask (__name__)
ma = Marshmallow(app)

class Director(db.Model):
    __tablename__ = 'director'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255))

class DirectorSchema (ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Director
        include_relationship = True
        load_instance = True
