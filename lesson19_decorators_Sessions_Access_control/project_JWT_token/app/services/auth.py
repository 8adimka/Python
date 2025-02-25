import calendar
import datetime
from flask import abort
import jwt
from app.services.users import UserService
from app.helpers.constants import JWT_ALGORITHM, JWT_SECRET


class AuthService:
    def __init__(self, user_secvice: UserService):
        self.user_service = user_secvice

    def generate_tokens(self, username, password, is_refresh=False):
        user = self.user_service.get_by_username(username)

        if user is None:
            raise abort(404)
        
        if not is_refresh:
            if not self.user_service.compare_passwords(user.password, password):
                abort(400)

        data = {"username": user.username,
                "role": user.role}
        
        # 30 minutes for access_token
        min30 = datetime.datetime.utcnow() + datetime.timedelta(minutes=30)
        data["exp"] = calendar.timegm(min30.timetuple())
        access_token = jwt.encode(data, JWT_SECRET, algorithm=JWT_ALGORITHM)

        # 130 days for refresh_token
        days130 = datetime.datetime.utcnow() + datetime.timedelta(days=130)
        data["exp"] = calendar.timegm(days130.timetuple())
        refresh_token = jwt.encode(data, JWT_SECRET, algorithm=JWT_ALGORITHM)

        return {"access_token": access_token,
                "refresh_token": refresh_token}

        
    def approve_refresh_token(self, refresh_token):
        data = jwt.decode(jwt=refresh_token, key=JWT_SECRET, algorithms=[JWT_ALGORITHM])
        username = data.get("username")

        return self.generate_tokens(username, None, is_refresh=True)        
        