# Просто: Напишите функцию `easy` которая 
# получает пароль в открытом виде и 
# возвращает хеш с использованием алгоритма md5
#
# Сложно: Напишите функцию `hard` которая 
# получает пароль в открытом виде и соль 
# и возвращает хеш с использованием алгоритма sha256

import hashlib

SALT = "Som3_SaL7"
SALT_encoded = b"Som3_SaL7" #-> Эквивалентно  SALT.encode('utf-8')

def easy(password):
    """Возвращает md5 хеш"""
    hash_digest = hashlib.md5(password.encode('utf-8')).hexdigest()
    return hash_digest

def hard(password, salt):
    return hashlib.pbkdf2_hmac(
        'sha256',
        password.encode('utf-8'),
        salt,
        1000
    )


def hard2(password, SALT_encoded):
    """Возвращает sha256 хеш с использованием соли"""
    hash_digest = hashlib.pbkdf2_hmac(
        'sha256',
        password.encode('utf-8'),
        SALT_encoded,
        1000  # Количество итераций
    )
    return hash_digest.hex() # Не проходит проверку изза .hex() в конце -> узнать про .hex() & .hexdigest()
