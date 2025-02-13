import calendar
import datetime
import jwt
from flask import request, abort, Flask
from flask_restx import Api, Resource

from app.constants import secret, algo

def generate_token(data):
    min30 = datetime.datetime.utcnow() +  datetime.timedelta(minutes=30)
    data["exp"] = calendar.timegm(min30.timetuple())
    return jwt.encode(data, secret, algorithm=algo)

def check_token(token):
    try:
        jwt.decode(token, secret, algorithms=[algo])
        return True
    except Exception:
        return False
    
def auth_required(func):
    def wrapper(*args, **kwargs):
        if 'Authorization' not in request.headers:
            abort(401)

        data = request.headers['Authorization']
        # data будет ~ 'Bearer eyJ0eXA..<token>'
        token = data.split("Bearer ")[-1]
        try:
            jwt.decode(token, secret, algorithms=[algo])
        except Exception as e:
            print("JWT Decode Exception", e)
            abort(401)
        return func(*args, **kwargs)
    
    return wrapper
