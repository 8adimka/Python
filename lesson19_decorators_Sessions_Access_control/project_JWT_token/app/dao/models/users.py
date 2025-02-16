from flask import Flask
from flask_marshmallow import Marshmallow
from app.database import db

app = Flask (__name__)
ma = Marshmallow(app)

class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(255))
    password = db.Column(db.String)
    role = db.Column(db.String(255))

class UserSchema (ma.SQLAlchemyAutoSchema):
    class Meta:
        model = User
        include_relationship = True
        load_instance = True
