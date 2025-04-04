# Напишите функцию `check_token`, которая проверяет токен. 
# Внимание, функция должна принимать 3 позиционных агрумента:
# токен, алгоритм и секрет.
# Функция должна возвращать:
# Декодированную информацию если токен удалось декодировать.
# И возвращайть False, если токен декодировать не удалось.

# В тестах мы проверим функцию,отправив ей верный и неверный токен.
import jwt

secret = 's3cR$eT'
algo = 'HS256'


def check_token(token, secret, algo):
    try:
        return jwt.decode(token, secret, algorithms=[algo])
    except Exception:
        return False
