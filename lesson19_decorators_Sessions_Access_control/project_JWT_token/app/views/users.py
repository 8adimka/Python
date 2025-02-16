from app.container import user_service
from flask import request
from flask_restx import Namespace, Resource
from app.database import db
from app.dao.models.users import UserSchema

users_ns = Namespace('users')

users_schema = UserSchema(many=True)
user_schema = UserSchema()

@users_ns.route ('/')
class UsersView(Resource):
    def get (self):
        """GET all users"""
        username = request.args.get('username')
        all_users = user_service.get_all(username)
        return users_schema.dump(all_users), 200
    
    def post(self):
        """Make new record - user"""
        try:
            data_json = request.json
            new_user = user_service.create(data_json)
            return user_schema.dump(new_user), 201, {"location":f"/users/{new_user.id}"}
    
        except Exception as e:
            return f'Error {e}', 404
        

@users_ns.route ('/<int:user_id>')
class UserView(Resource):
    def get (self, user_id):
        """GET user by ID"""
        user = user_service.get_one(user_id)
        return user_schema.dump(user), 200
    
    def put(self, user_id):
        """PUT user by ID"""
        data_json = request.json
        data_json['id']=user_id

        user = user_service.update(data_json)

        return user_schema.dump(user), 200
    
    def patch(self, user_id):
        """PATCH user by ID"""
        data_json = request.json
        data_json['id']=user_id

        user = user_service.update_partial(data_json)

        return user_schema.dump(user), 204

    def delete(self, user_id):
        """Delete user by ID"""
        user_service.delete(user_id)
        return {"message": "Пользователь удален"}, 204
