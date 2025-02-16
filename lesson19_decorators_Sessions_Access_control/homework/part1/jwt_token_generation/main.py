# У вас есть словарь, который содержит 
# данные о пользователе. На его основе 
# сгенерируйте токен. 
#
# В качестве секрета используйте слово 's3cR$eT',
# В качестве алгоритма формирования токена используйте 'HS256'.
# Сгенерированный токен запишите в переменную access_token.
import jwt

secret = 's3cR$eT'
algo = 'HS256'

def token_generator (data):
    return jwt.encode(data, secret, algorithm=algo)

data = {
        "username": "Skypro",
        "role": "admin"
        }

#TODO напишите Ваш код здесь
access_token = token_generator (data)