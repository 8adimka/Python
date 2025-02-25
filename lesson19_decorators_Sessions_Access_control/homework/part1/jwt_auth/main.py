# В данном задании у Вас уже имеется сгенерированный токен,
# выбран алгоритм а также секрет для flask приложения.
# Вам предстоит написать декоратор `auth_required`, 
# проверяющий авторизацию по выданному токену.
# Проверять имеется ли пользователь 
# с таким токеном в базе данных, в данном задании не нужно.
# Достаточно просто позволить выполнение декорируемой функции при
# успешном декодировании токена.
#
# При тестировании Вашего решения на приложение 
# будут посылаться GET-запрос без авторизации 
# и POST-запрос c заголовком:
# Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VybmFtZSI6IlNreXBybyIsInJvbGUiOiJhZG1pbiJ9.fMPkh9GNQMlLRxO0PmvCjUPPwX0t4CM5Wk4ATt35mNY
# Декорируемая функция должна возвращать код 401 если заголовок Authorization
# отсутствует, а также код 401 если токен неверный или раскодировать его не удалось.
# Если токен удалось раскодировать, декорируемая функция должна быть выполнена.

import jwt
from flask import request, abort, Flask
from flask_restx import Api, Resource

algo = 'HS256'
secret = 's3cR$eT'
token = "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VybmFtZSI6IlNreXBybyIsInJvbGUiOiJhZG1pbiJ9.fMPkh9GNQMlLRxO0PmvCjUPPwX0t4CM5Wk4ATt35mNY"

def auth_required(func):
    def wrapper(*args, **kwargs):
        # Проверяем наличие заголовка Authorization
        auth_header = request.headers.get('Authorization')
        if not auth_header:
            abort(401)

        # Проверяем префикс Bearer
        token_parts = auth_header.split()
        if len(token_parts) != 2 or token_parts[0] != 'Bearer':
            abort(401)

        # Декодируем токен
        token = token_parts[1]
        try:
            jwt.decode(token, secret, algorithms=[algo])
        except Exception as e:
            print("JWT Decode Exception:", e)
            abort(401)
        
        return func(*args, **kwargs)
    return wrapper

# Ниже следует код инициализации фласк приложения.
# Из которого следует что GET-запрос на адрес books могут делать все
# пользователи, а POST-запросы разрешены только авторизованным
# пользователям. Исходя из этой логики проверьте работу 
# своего декоратора, запустив приложение. Менять этот код не нужно

app = Flask(__name__)
app.config['JSON_AS_ASCII'] = False
app.url_map.strict_slashes = False
api = Api(app)
book_ns = api.namespace('')


@book_ns.route('/books')
class BooksView(Resource):
    def get(self):
        return [], 200

    @auth_required
    def post(self):
        return "", 201


if __name__ == '__main__':
    app.run(debug=False)
