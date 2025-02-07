from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from flask_restx import Api, Resource
from marshmallow import Schema, fields
from flask_marshmallow import Marshmallow

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////tmp/test.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['JSON_AS_ASCII'] = False
db = SQLAlchemy(app)
ma = Marshmallow(app)

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


class UserSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = User
        load_instance = True


users_schema = UserSchema(many=True)
user_schema = UserSchema()

# этот код наполняет БД
with app.app_context():
    db.drop_all()
    db.create_all()
    movies = [User(**user) for user in user_data]
    db.session.add_all(movies)
    db.session.commit()
    print("База данных создана")

api = Api(app)
users_ns = api.namespace('users')


@users_ns.route("/")
class UsersView(Resource):
    def get(self):
        all_users = User.query.all()
        return users_schema.dump(all_users), 200
    
@users_ns.route("/<int:user_id>")
class UsersView(Resource):
    def get(self, user_id):
        user = User.query.get_or_404(user_id)
        return user_schema.dump(user), 200


app.run()