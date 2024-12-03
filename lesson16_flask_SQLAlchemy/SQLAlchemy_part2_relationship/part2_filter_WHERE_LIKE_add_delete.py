from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import or_, desc, func
from sqlalchemy.orm import relationship

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///:memory:"  # Для работы в базе-данных *in memory* без файлов и сохранения -> :memory:
db = SQLAlchemy(app)

class User(db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    passport_number = db.Column(db.String(4), unique=True)
    name = db.Column(db.String(100), nullable=False) #Не допускается null пустая ячейка, пропуск
    age = db.Column(db.Integer, db.CheckConstraint("age >= 18")) #Проверка выполнения условия
    group_id = db.Column(db.Integer, db.ForeignKey("groups.id"))

    group = relationship("Group", back_populates="users")

class Group(db.Model):
    __tablename__ = "groups"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))

    users = relationship("User", back_populates="group")

# Использование контекста приложения для работы с базой данных
with app.app_context():
    db.create_all()

    # Создание и добавление данных в базу данных
    group_1 = Group(name="Group #1")
    group_2 = Group(name="Group #2")

    user_1 = User(passport_number = 1234, name="John", age=30, group=group_1)
    user_2 = User(name="Kate", age=32, group=group_2)
    user_3 = User(passport_number = 123, name="Max", age=34, group=group_1)
    user_4 = User(name="Lily", age=28, group=group_1)
    user_5 = User(name="Mary", age=26, group=group_2)
    user_6 = User(name="Vas", age=31, group=group_2)

    db.session.add_all([
        user_1, 
        user_2,
        user_3,
        user_4,
        user_5,
        user_6
        ])
    db.session.commit()

    user_with_group = User.query.get(1)
    print(user_with_group.group.name)
    print(user_with_group.name)

    # Запросы данных

# SELECT users.id AS users_id и т.д. ВСЁ
# FROM users 
# WHERE users.name = ? (условие подставляется прямо при обработке - "Max")
# Результат: Max   
    query = db.session.query(User).filter(User.name == "Max")
    print(f"Запрос: {query}")
    print(f"Результат: {query.first().name}")

# SELECT users.id AS users_id, ВСЁ остальное -> tablename.columname AS tablename_columname
# FROM users 
# WHERE users.name = "Max"
# Результат: <User 2>
    query = db.session.query(User).filter(User.name == "Max")
    print(f"Запрос: {query}")
    print(f"Результат: {query.one()}")

# Запрос: SELECT users.id AS users_id, users.passport_number AS users_passport_number...
# FROM users 
# WHERE users.id <= 5 AND users.age > 20
# Результат: [<User 1>, <User 2>, <User 3>, <User 4>, <User 5>]
    query = db.session.query(User).filter(User.id <=5, User.age>20)
    print(f"Запрос: {query}")
    print(f"Результат: {query.all()}")

# Запрос: SELECT users.id AS users_id, users.passport_number AS users_passport...
# FROM users 
# WHERE users.name LIKE "M%"
# Результат: [<User 2>, <User 5>]
    query = db.session.query(User).filter(User.name.like("M%"))
    print(f"Запрос: {query}")
    print(f"Результат: {query.all()}")

# Запрос: SELECT users.id AS users_id, users.passport_number AS users... ВСЁ
# FROM users 
# WHERE users.id <= ? OR users.age > ? (*ИЛИ*OR* условия подставляются прямо при обработке запроса)
# Результат: [<User 1>, <User 2>, <User 3>, <User 4>, <User 5>, <User 6>] (либо под одно, либо под другое условие подходят все)
    query = db.session.query(User).filter(or_(User.id <=5, User.age > 20))
    print(f"Запрос: {query}")
    print(f"Результат: {query.all()}")

# Запрос: SELECT users.id AS users_id, users.passport_number AS users_passport_number, users.name AS users_name, users.age AS users_age, users.group_id AS users_group_id 
# FROM users 
# WHERE users.passport_number IS NULL
# Результат: [<User 3>, <User 4>, <User 5>, <User 6>]
    query1 = db.session.query(User).filter(User.passport_number == None)
    print(f"Запрос: {query1}")
    print(f"Результат: {query1.all()}")

# Запрос: SELECT users.id AS users_id, users.passport_number AS users_passport_number, users.name AS users_name, users.age AS users_age, users.group_id AS users_group_id 
# FROM users 
# WHERE users.passport_number IS NOT NULL
# Результат: [<User 1>, <User 2>]
    query2 = db.session.query(User).filter(User.passport_number != None)
    print(f"Запрос: {query2}")
    print(f"Результат: {query2.all()}")

# Запрос: SELECT users.id AS users_id, users.passport_number AS users_passport_number, users.name AS users_name, users.age AS users_age, users.group_id AS users_group_id 
# FROM users 
# WHERE users.id IN (__[POSTCOMPILE_id_1])
# Результат: [<User 1>, <User 3>, <User 4>]
    query = db.session.query(User).filter(User.id.in_([1,3,4]))
    print(f"Запрос: {query}")
    print(f"Результат: {query.all()}")

# Запрос: SELECT users.id AS users_id, users.passport_number AS users_passport_number...
# FROM users 
# WHERE (users.id NOT IN (__[POSTCOMPILE_id_1]))
# Результат: [<User 2>, <User 5>, <User 6>]
    query = db.session.query(User).filter(User.id.notin_([1,3,4]))
    print(f"Запрос: {query}")
    print(f"Результат: {query.all()}")

# Запрос: SELECT users.id AS users_id, users.passport_number AS users_passport_number, users.name AS users_name, users.age AS users_age, users.group_id AS users_group_id 
# FROM users 
# WHERE users.id BETWEEN ? AND ?
# Результат: [<User 1>, <User 2>, <User 3>, <User 4>]
    query = db.session.query(User).filter(User.id.between(1,4))
    print(f"Запрос: {query}")
    print(f"Результат: {query.all()}")

# Запрос: SELECT users.id AS users_id, users.passport_number AS users_passport_number, users.name AS users_name, users.age AS users_age, users.group_id AS users_group_id 
# FROM users
# LIMIT ? OFFSET ?
# Результат: [<User 1>, <User 2>]
    query = db.session.query(User).limit(2)
    print(f"Запрос: {query}")
    print(f"Результат: {query.all()}")

# Запрос: SELECT users.id AS users_id, users.passport_number AS users_passport_number, users.name AS users_name, users.age AS users_age, users.group_id AS users_group_id 
# FROM users
#  LIMIT ? OFFSET ?
# Результат: [<User 4>, <User 5>]
    query = db.session.query(User).limit(2).offset(3)
    print(f"Запрос: {query}")
    print(f"Результат: {query.all()}")


# Запрос: SELECT users.id AS users_id, users.passport_number AS users_passport_number, users.name AS users_name, users.age AS users_age, users.group_id AS users_group_id 
# FROM users ORDER BY users.id
# Результат: [<User 1>, <User 2>, <User 3>, <User 4>, <User 5>, <User 6>]
    query = db.session.query(User).order_by(User.id)
    print(f"Запрос: {query}")
    print(f"Результат: {query.all()}")

# Запрос: SELECT users.id AS users_id, users.passport_number AS users_passport_number, users.name AS users_name, users.age AS users_age, users.group_id AS users_group_id 
# FROM users
# ORDER BY users.id DESC
# Результат: [<User 6>, <User 5>, <User 4>, <User 3>, <User 2>, <User 1>]
    query = db.session.query(User).order_by(desc(User.id)) #DESC от большего к меньшему
    print(f"Запрос: {query}")
    print(f"Результат: {query.all()}")


# Запрос: SELECT users.name AS users_name, groups.name AS groups_name 
# FROM users JOIN groups ON groups.id = users.group_id  *(Это INNER JOIN)
# Результат: [('John', 'Group #1'), ('Max', 'Group #1'), ('Lily', 'Group #1'), ('Kate', 'Group #2'), ('Mary', 'Group #2'), ('Vas', 'Group #2')]
    query = db.session.query(User.name, Group.name).join(Group) #*(Это INNER JOIN) А если нужен LEFT JOIN -> .join(Group, outer=True)
    print(f"Запрос: {query}")
    print(f"Результат: {query.all()}")


# Запрос: SELECT count(users.id) AS count_1 
# FROM users JOIN groups ON groups.id = users.group_id 
# WHERE groups.id = ? GROUP BY groups.id
# Результат: 3
    query = db.session.query(func.count(User.id)).join(Group).filter(Group.id == 1).group_by(Group.id)
    print(f"Запрос: {query}")
    print(f"Результат: {query.scalar()}") #Получаем скалярную величину, которую выводим


    # Изменение (update) значений в таблицах
    user = User.query.get(2)
    print (user.name)

    user.name = "Updated name"
    db.session.add(user)
    db.session.commit()

    user = User.query.get(2)
    print (user.name)


    # Удаление записи по ID
    user = User.query.get(2)
    db.session.delete(user)
    db.session.commit()
#True
    user = User.query.get(2)
    print (user is None)


    # Запросы на удаление данных по условию
    db.session.query(User).filter(User.name == "Lily").delete()
    db.session.commit()
#User -> []
    user = User.query.filter(User.name == "Lily").all()
    print (f"User -> {user}")


if __name__ == '__main__':
    app.run()
