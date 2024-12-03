from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import relationship

app = Flask (__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///:memory:" 
# Для работы в базе-данных *in memory* без файлов и сохранения -> :memory:
# SQLALCHEMY_DATABASE_URI - обязательно большие буквы
db = SQLAlchemy(app)

class User(db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False) #Не допускается null пустая ячейка, пропуск
    age = db.Column(db.Integer) #Тип данных в SQLAlchemy чувствителен к регистру. Правильно -> db.Integer
    group_id = db.Column(db.Integer, db.ForeignKey("groups.id")) # SQLAlchemy чувствителен к регистру. Правильно -> db.ForeignKey

    group = relationship("Group", back_populates="users") #back_populates - создаёт обратную связь и по группе также можно получить пользователей в ней

class Group(db.Model):
    __tablename__ = "groups"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))

    users = relationship("User", back_populates="group")

# Использование контекста приложения для работы с базой данных
with app.app_context():
    db.create_all()

    # Создание и добавление данных в базу данных (2 пособа)
    group_1 = Group(name="Group #1")
    user_1 = User(name="John", age=30, group=group_1)
    user_2 = User(name="Vas", age=32, group=group_1)

    db.session.add_all([user_1,user_2])


    student_1 = User(name="Nick", age=30)
    student_2 = User(name="Ken", age=33)
    group_students = Group(name="Students #1", users=[student_1,student_2])

    db.session.add(group_students)

    user_with_group = User.query.get(3)
    print(user_with_group.group.name)
    print(user_with_group.name)


if __name__ == '__main__':
    app.run()

