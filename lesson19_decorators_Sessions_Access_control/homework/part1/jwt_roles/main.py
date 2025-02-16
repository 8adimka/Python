# В данном задании у Вас также уже имеется сгенерированный токен.
# - eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VybmFtZSI6IlNreXBybyIsInJvbGUiOiJhZG1pbiJ9.fMPkh9GNQMlLRxO0PmvCjUPPwX0t4CM5Wk4ATt35mNY

# Данный токен содержит объект user с аттрибутами
# - username 
# - role
# Кроме того, выбран алгоритм и имеется секрет для flask приложения.
#
# Вам предстоит написать декоратор `admin_required`, 
# который проверяет роль пользователя.
# Проверять имеется ли пользователь 
# с таким токеном в базе данных, в данном задании не нужно.
# Достаточно просто удостоверится, что аттрибут role 
# предоставленного токена соответсвует значению 'admin'и позволить выполнение 
# декорируемой функции.
#
# При тестировании Вашего решения на приложение 
# будут посылаться GET-запрос без авторизации 
# и POST-запрос c заголовком:
# Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VybmFtZSI6IlNreXBybyIsInJvbGUiOiJhZG1pbiJ9.fMPkh9GNQMlLRxO0PmvCjUPPwX0t4CM5Wk4ATt35mNY
#
# Декорируемая функция должна возвращать:
# - Ответ с кодом 401 если заголовок Authorization
#   отсутствует, токен неверный или раскодировать его не удалось.
# - Ответ с кодом 403 если роль пользователя не соответствует значению 'admin'.
#
# Если токен удалось раскодировать, и роль соответствует ожидаемой
# декорируемая функция должна быть выполнена.

from flask import Flask, abort, request
from flask_restx import Api, Resource
import jwt

algo = 'HS256'
secret = 's3cR$eT'

def admin_required(func):
    def wrapper (*args, **kwargs):
        data = data = request.headers.get('Authorization')
        if not data:
            abort (401)
        token = data.split("Bearer ")[-1]
        try:
            user = jwt.decode(token, secret, algorithms=[algo])
            role = user.get("role")
            print (user['username'])
        except Exception as e:
            print("JWT Decode Exception:", e)
            abort(401)
        if role != 'admin':
            abort (403)
        return func (*args, **kwargs)
    return wrapper
        
            

# Ниже следует код инициализации фласк приложения.
# Из которого следует что GET-запрос на адрес books могут делать все
# пользователи, а POST-запросы разрешены только администраторам.
# Исходя из этой логики проверьте работу 
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

    @admin_required
    def post(self):
        return "", 201


if __name__ == '__main__':
    app.run(debug=False)

