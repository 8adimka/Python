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


# Подготовка данных
group_1 = Group(name="Group #1")
group_2 = Group(name="Group #2")

with app.app_context():
    db.create_all()
    db.session.add_all([group_1,group_2])
    db.session.commit()

user_1 = User(passport_number = 1234, name="John", age=30, group=group_1)
user_2 = User(name="Kate", age=32, group=group_2)
user_3 = User(passport_number = 123, name="Max", age=34, group=group_1)
user_4 = User(name="Lily", age=28, group=group_1)
user_5 = User(name="Mary", age=26, group=group_2)
user_6 = User(name="Vas", age=31, group=group_2)


# Открываем сессию - в момент ёё закрытия будет произведено(2):
# 1)FLUSH(записать в базу и можно работать, но можно и откатить ещё) и
# 2)COMMIT (подтвердить изменения и уже не откатишь)
# with db.session.begin():
with app.app_context():
    try:
        db.session.add (user_3)
        db.session.add (user_2)

        nested = db.session.begin_nested()
        try:
            db.session.add (user_5)
            db.session.add (user_4)
            # raise Exception("database exception") #например, если ловим тут ошибку (это мы исскуственно вызываем ошибку)
            nested.commit()
        
        except Exception as e:
            print (f"Error: {e}")
            nested.rollback()

        # raise Exception("unexpected exception") #исскуственно вызываем ошибку
        db.session.commit()
    
    except Exception as e: 
    # Теперь,если мы получим ошибку во вложенной транзакции,
    # мы обработаем ошибку вложенной транзакции,
    # если в основной, то перехватим и обработаем ошибку основной и откатим результат.
        db.session.rollback()
            
        

    # user_with_group = User.query.get(1)
    # print(user_with_group.group.name)
    # print(user_with_group.name)
    users = User.query.all()
    print(users)
    print (users[0].name, users[1].name, users[3].name)
    for u in users:
        print(u.name, u.id)