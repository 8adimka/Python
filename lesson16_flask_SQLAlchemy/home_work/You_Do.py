from flask import Flask, render_template, request, session
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import or_, desc, func
from sqlalchemy.orm import relationship
import json
from datetime import datetime

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:////home/v/Python/lesson16_flask_SQLAlchemy/home_work/User_Executor.db"
db = SQLAlchemy(app)
app.secret_key = '123'  # Обязательна настройка секретного ключа для работы сессий


class User (db.Model):
    __tablename__ = "users"

    id = db.Column (db.Integer, primary_key=True)
    first_name = db.Column(db.String (100), nullable = False)
    last_name = db.Column(db.String(100))
    age = db.Column(db.Integer, db.CheckConstraint("age>=16"))
    email = db.Column(db.String(150))
    role = db.Column(db.String(100))
    phone = db.Column(db.String(100))

class Order(db.Model):
    __tablename__ = "orders"

    id = db.Column (db.Integer, primary_key=True)
    name = db.Column(db.String (100))
    description = db.Column(db.String(1000), nullable = False)
    start_date = db.Column(db.Date)
    end_date = db.Column(db.Date)
    address = db.Column(db.String(150))
    price = db.Column(db.Integer)

    customer_id = db.Column(db.Integer, db.ForeignKey("users.id"))
    executor_id = db.Column(db.Integer, db.ForeignKey("users.id"))


class Offer(db.Model):
    __tablename__ = "offers"

    id = db.Column (db.Integer, primary_key=True)

    order_id = db.Column(db.Integer, db.ForeignKey("orders.id"))
    executor_id = db.Column(db.Integer, db.ForeignKey("users.id"))

# Создание таблиц
with app.app_context():
    db.drop_all()  # Удаление всех таблиц
    db.create_all()

# Загрузка данных из JSON файлов
with open("/home/v/Python/lesson16_flask_SQLAlchemy/home_work/users.json") as file:
    users_json = json.load(file)

with open("/home/v/Python/lesson16_flask_SQLAlchemy/home_work/orders.json") as file:
    orders_json = json.load(file)

with open("/home/v/Python/lesson16_flask_SQLAlchemy/home_work/offers.json") as file:
    offers_json = json.load(file)

# Добавление данных в таблицы
with app.app_context():
    for user in users_json:
        u = User(**user)
        db.session.add(u)
    for order in orders_json:
        o = Order(name = order["name"], description=order["description"], start_date=datetime.strptime(order["start_date"], "%m/%d/%Y").date(),end_date=datetime.strptime(order["end_date"], "%m/%d/%Y").date(),address=order["address"],price=order["price"],customer_id=order["customer_id"],executor_id=order["executor_id"])
        db.session.add(o)
    for offer in offers_json:
        of = Offer(**offer)
        db.session.add(of)
    db.session.commit()

# @app.route('/users/<int:user>/')
# def user_page(user=None):
#     if user is None:
#         with app.app_context():
#             user_data = db.session.query(User).all()
#     else:
#         with app.app_context():
#             user_data = db.session.query(User).get(user)
#             if not user_data:
#                 return f"User with ID {user} not found", 404

#             # Преобразование объекта в словарь
#             user_dict = {
#                 "first_name": user_data.first_name,
#                 "last_name": user_data.last_name,
#                 "age": user_data.age,
#                 "email": user_data.email,
#                 "phone": user_data.phone,
#                 "role": user_data.role,
#             }
#     return render_template('users.html', **user_dict)

@app.route('/users/')
def users_page():
    with app.app_context():
        user_data = db.session.query(User).all()
        if not user_data:
            return f"Users not found", 404
        else:
            results = user_data

    return render_template('users.html', results=results)

@app.route('/users/<int:user>/')
def user_page(user=None):
    with app.app_context():
        user_data = db.session.query(User).get(user)

    return render_template('user.html', user_data=user_data)

@app.route('/user/new/')
def new_user_page():
    result = None
    with app.app_context():
        if request.args.get('first_name', '')=='':
            return render_template('new_user.html', result=result)
        else:
            new_user = User (first_name = request.args.get('first_name', ''),
                            last_name = request.args.get('last_name', ''),
                            age = request.args.get('age', ''),
                            email = request.args.get('email', ''),
                            role = request.args.get('role', ''),
                            phone = request.args.get('phone', ''))
            db.session.add(new_user)
            db.session.commit()
            result = True

    return render_template('new_user.html', result=result)

@app.route('/user/change/')
def change_user_page():
    with app.app_context():
        result = None
        # Если данные ещё не отправлены, загружаем форму
        if request.args.get('first_name', '') == '':
            user_id = request.args.get('user_id', '')
            if not user_id:
                return "No user ID received", 400
            # Сохраняем user_id в сессии
            session['user_id'] = user_id
            return render_template('change_user.html', result=result, user_id=user_id)
        else:
            # Если данные отправлены, обновляем пользователя
            user_id = session.get('user_id', None)
            if not user_id:
                return "No user ID found in session", 400
            
            # Находим пользователя в базе данных
            change_user = db.session.query(User).get(user_id)
            if not change_user:
                return f"User with ID {user_id} not found", 404
            
            # Обновляем поля пользователя
            change_user.first_name = request.args.get('first_name', '')
            change_user.last_name = request.args.get('last_name', '')
            change_user.age = request.args.get('age', '')
            change_user.email = request.args.get('email', '')
            change_user.role = request.args.get('role', '')
            change_user.phone = request.args.get('phone', '')

            # Сохраняем изменения
            db.session.commit()
            result = True
            return render_template('change_user.html', result=result)
        
    return render_template ('change_user.html', result=result)

@app.route('/orders/<int:order>/')
def order_page(order):
    with app.app_context():
        order_data = db.session.query(Order).get(order)
        if not order_data:
            return f"User with ID {user} not found", 404
    return f"{order_data.name} - {order_data.price} US,<br/> description - {order_data.description}. Начало - {order_data.start_date} закончить до - {order_data.end_date}"

@app.route('/offers/<int:offer>/')
def offer_page(offer):
    with app.app_context():
        offer_data = db.session.query(Offer).get(offer)
        if not offer_data:
            return f"User with ID {user} not found", 404
    return f"order_id - {offer_data.order_id}, executor_id - {offer_data.executor_id}"


if __name__ == "__main__":
    app.run()



