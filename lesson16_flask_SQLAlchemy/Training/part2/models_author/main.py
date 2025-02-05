# Напишите модели автор(Author) и книга (Book)
# в соответствии с uml (схема в файле tables.png в папке задания)
#
#
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import prettytable
from sqlalchemy.orm import relationship, joinedload
from sqlalchemy import text

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db: SQLAlchemy = SQLAlchemy(app)


class Author(db.Model):
    __tablename__ = "author"
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(100))
    last_name = db.Column(db.String(100))

    books = relationship ("Book", back_populates='author')


class Book(db.Model):
    __tablename__ = "book"
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200))
    copyright = db.Column(db.Integer)
    author_id = db.Column(db.Integer, db.ForeignKey('author.id'))

    author = relationship ("Author", back_populates='books')

with app.app_context():
    db.create_all()
    book_1 = Book(title = "up&down&up_again")
    book_2 = Book(title = "STICK'n'RoCk", copyright=6)
    author_1 = Author(first_name='Robert', last_name='Rodrigez', books = [book_1, book_2])
    db.session.add(author_1)
    db.session.commit()

    session = db.session()
    cursor_author = session.execute(text("SELECT * from author")).cursor

    mytable = prettytable.from_db_cursor(cursor_author)
    cursor_book = session.execute(text("SELECT * from book")).cursor

    mytable2 = prettytable.from_db_cursor(cursor_book)

    my_request = db.session.query(Book).options(joinedload(Book.author)).all()
    my_request2 = db.session.query(Book).join(Author).all()

    # book = Book.query.get(1)

if __name__ == '__main__':
    print(mytable)
    print(mytable2)
    print('_______________')
    print('_______________')
    for b in my_request:
        print (b.title, b.author.first_name, b.author.last_name)
    print('_______________')
    for book in my_request2:
        print (book.title)

    # if book and book.author:
    #     print(f'Книга - {book.title}, \nАвтор - {book.author.first_name} {book.author.last_name}')
    # else:
    #     print("Ошибка: у книги нет автора или она не найдена.")

    
