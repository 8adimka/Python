from flask import Flask, jsonify
from flask_sqlalchemy import SQLAlchemy
from marshmallow import Schema, fields

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////tmp/test.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['JSON_AS_ASCII'] = False
db = SQLAlchemy(app)

user_data = [
    {'id': 1, 'first_name': 'Hudson', 'last_name': 'Pauloh', 'age': 31, 'email': 'elliot16@mymail.com',
     'role': 'customer', 'phone': '6197021684'},
    {'id': 2, 'first_name': 'George', 'last_name': 'Matter', 'age': 41, 'email': 'lawton46@mymail.com',
     'role': 'executor', 'phone': '8314786677'},
    {'id': 3, 'first_name': 'Grant', 'last_name': 'Traviser', 'age': 23, 'email': 'tobias45@mymail.com',
     'role': 'customer', 'phone': '9528815998'}
]


class User(db.Model):
    __tablename__ = 'movie'
    id = db.Column(db.Integer, primary_key=True)
    age = db.Column(db.Integer)
    role = db.Column(db.String(255))
    first_name = db.Column(db.String(255))
    last_name = db.Column(db.String(255))
    email = db.Column(db.String(255))
    phone = db.Column(db.String(255))


class UserSchema(Schema):
    ...


user_schema = UserSchema(many=True)

# этот код наполняет БД, не трогайте е
with app.app_context():
    db.drop_all()
    db.create_all()
    movies = [User(**user) for user in user_data]
    db.session.add_all(movies)
    db.session.commit()
    print("База данных создана")


@app.route("/users")
def get_users():

    ...


app.run()