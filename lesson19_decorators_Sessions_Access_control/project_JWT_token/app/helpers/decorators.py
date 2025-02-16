import jwt
from flask import request, abort
from app.helpers.constants import JWT_SECRET, JWT_ALGORITHM

def auth_required(func):
    def wrapper(*args, **kwargs):
        if "Authorization" not in request.headers:
            abort(401)
        
        data = request.headers["Authorization"]
        # data будет ~ 'Bearer eyJ0eXA..<token>'
        token = data.split("Bearer ") [-1]

        try:
            jwt.decode(token, JWT_SECRET, algorithms=[JWT_ALGORITHM])
        except Exception as e:
            print("JWT Decode Exception", e)
            abort(401)

        return func(*args, **kwargs)
    return wrapper


def admin_required(func):
    def wrapper (*args, **kwargs):
        data = request.headers.get('Authorization')
        if not data:
            abort (401)
        token = data.split("Bearer ")[-1]
        role = None
        try:
            user = jwt.decode(token, JWT_SECRET, algorithms=[JWT_ALGORITHM])
            role = user.get("role", "user") #Извлекаем роль нашего пользователя, если оно не задано, присваевается стандартное "user"
            print (user['username'])
        except Exception as e:
            print("JWT Decode Exception:", e)
            abort(401)

        if role != 'admin':
            abort (403)
            
        return func (*args, **kwargs)
    return wrapper

