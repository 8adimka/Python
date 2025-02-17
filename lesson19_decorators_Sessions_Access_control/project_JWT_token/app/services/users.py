import base64
import hashlib
import hmac
from app.dao.users import UserDAO
from app.helpers.constants import PWD_ITERATIONS, PWD_SALT


class UserService:
    def __init__(self, dao: UserDAO):
        self.dao = dao

    def get_one(self, user_id):
        return self.dao.get_one(user_id)
    
    def get_all(self):
        return self.dao.get_all()
    
    def get_by_username(self, username):
        return self.dao.get_by_username(username)

    def create (self, data):
        data["password"] = self.generate_password(data["password"])
        return self.dao.create(data)

    def update (self, data):
        user_id = data.get("id")
        user = self.dao.get_one(user_id)
        user.username = data.get("username")
        user.password = self.generate_password(data["password"])
        user.role = data.get("role")

        self.dao.update(user)

    def update_partial(self, data):
        user_id = data.get("id")
        user = self.dao.get_one(user_id)
        if "username" in data:
            user.username = data.get("username")
        if "password" in data:
            user.password = self.generate_password(data["password"])
        if "role" in data:
            user.role = data.get("role")

        self.dao.update(user)

    def delete(self, user_id):
        self.dao.delete(user_id)

    def generate_password(self, password):
        hash_digest = hashlib.pbkdf2_hmac('sha256',
                                          password.encode('utf-8'),
                                          PWD_SALT,
                                          PWD_ITERATIONS)
        return base64.b64encode(hash_digest)
    
    def compare_passwords(self, password_hash, other_password) -> bool:
        decoded_digest = base64.b64decode(password_hash)

        hash_digest = hashlib.pbkdf2_hmac(
            'sha256',
            other_password.encode('utf-8'),
            PWD_SALT,
            PWD_ITERATIONS
        )
        return hmac.compare_digest(decoded_digest, hash_digest)
    
