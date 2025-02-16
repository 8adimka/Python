from flask import request
from app.dao.models.users import User, UserSchema

#CRUD

users_schema = UserSchema(many=True)
user_schema = UserSchema()

class UserDAO:
    def __init__(self, session):
        self.session = session

    def get_one(self,user_id):
        """GET user by ID"""
        return self.session.query(User).get(user_id)
    
    def get_all(self):
        """GET all users"""
        return self.session.query(User).all()

    def get_by_username(self, username):
        """GET filtered users"""
        return self.session.query(User).filter(User.username == username).all()
    
    def create (self, data):
        """Make new record - user"""
        new_user = user_schema.load(data)
        self.session.add(new_user)
        self.session.commit()
        return new_user

    def update (self, user):
        """PUT user by ID"""
        self.session.add(user)
        self.session.commit()
        return user

    def delete(self, user_id):
        """Delete user by ID"""
        user = self.get_one(user_id)
        self.session.delete(user)
        self.session.commit()


