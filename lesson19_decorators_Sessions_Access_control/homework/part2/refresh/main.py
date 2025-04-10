# Написать функцию `generate_jwt` которая 
# генерирует access_token и refresh_token.
# В качестве аргумента функция должна принимать словарь вида user_obj.
# Для формирования токена используйте алгоритм 'HS256' и ключ 's3cR$eT'.
# В access и в refresh токене должна содержаться информация об:
# 1. имени пользователя ('username')
# 2. роли ('role')
# 3. времени действия токена ('exp')
# Время действия access токена должно составлять 30 с момента получения
# Время действия refresh токена - 130 дней c момента получения

import calendar
import datetime

import jwt


user_obj = {
    "username": 'test_user',
    "role": 'admin'
}

def generate_jwt(user_obj):
    # 30 minutes for access_token
    min30 = datetime.datetime.utcnow() + datetime.timedelta(minutes=30)
    user_obj["exp"] = calendar.timegm(min30.timetuple())
    access_token = jwt.encode(user_obj, 's3cR$eT', algorithm='HS256')

    # 130 days for refresh_token
    days130 = datetime.datetime.utcnow() + datetime.timedelta(days=130)
    user_obj["exp"] = calendar.timegm(days130.timetuple())
    refresh_token = jwt.encode(user_obj, 's3cR$eT', algorithm='HS256')

    return {"access_token": access_token,
            "refresh_token": refresh_token}