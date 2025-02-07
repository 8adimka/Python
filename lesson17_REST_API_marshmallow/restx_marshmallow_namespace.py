from flask import Flask, request, jsonify
from flask_restx import Api, Resource
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import relationship
from sqlalchemy import ForeignKey
from flask_marshmallow import Marshmallow
from marshmallow import fields

# Инициализация приложения Flask
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False  # Отключаем отслеживание изменений в объектах моделей (например, изменения атрибутов)

db = SQLAlchemy(app)
ma = Marshmallow(app)  # ✅ Инициализация Marshmallow

# 🔹 Определение моделей SQLAlchemy
class Book(db.Model):
    __tablename__ = 'books'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    year = db.Column(db.Integer)
    author_id = db.Column(db.Integer, ForeignKey('authors.id'))

    author = relationship("Author", back_populates='books')

class Author(db.Model):
    __tablename__ = 'authors'
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(100))
    last_name = db.Column(db.String(100), nullable=False)

    books = relationship('Book', back_populates='author')

# 🔹 Схемы для сериализации (автоматические)
class AuthorSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Author
        include_relationships = True 
        load_instance = True

class BookSchema(ma.SQLAlchemyAutoSchema):
    author = fields.Nested(AuthorSchema)  # Вложенная сериализация
    class Meta:
        model = Book
        include_relationships = True 
        include_fk = True
        load_instance = True

# 🔹 API-эндпоинты (REST API)
author_schema = AuthorSchema()
authors_schema = AuthorSchema(many=True)

book_schema = BookSchema()
books_schema = BookSchema(many=True)

api = Api(app)  # ✅ Подключаем Flask-RESTx
books_ns = api.namespace('books') # Наш адрес начинается с /books
authors_ns = api.namespace('authors')

# 🔹 Создание базы данных
with app.app_context():
    db.create_all()

    # Добавляем тестовые данные
    author1 = Author(first_name="George", last_name="Orwell")
    book1 = Book(name="1984", year=1949, author=author1)
    book2 = Book(name="Animal Farm", year=1945, author=author1)
    author2 = Author(first_name="Joan", last_name="Rouling")
    book3 = Book(name="Harry Potter", year=1992, author=author2)

    db.session.add_all([author1, book1, book2])
    db.session.add_all([author2, book3])
    db.session.commit()

@books_ns.route('/') # / + books + /
class BooksView(Resource):
    def get(self):
        try:
            """Получить все книги"""
            all_books = db.session.query(Book).all()
            return books_schema.dump(all_books), 200

        except Exception as e:
            return f'Error {e}', 404
    
    def post(self):
        try:
            data_json = request.json
            new_book = book_schema.load(data_json) # Book(**data_json) Создаём объект из JSON
            db.session.add(new_book)
            db.session.commit()
            return book_schema.dump(new_book), 201
    
        except Exception as e:
            return f'Error {e}', 404
    
@books_ns.route('/<int:book_id>/')
class BookView(Resource):
    def get(self, book_id):
        """Получить книгу по ID"""
        book = Book.query.get_or_404(book_id)
        return book_schema.dump(book), 200
    
    def put(self, book_id):
        book = db.session.query(Book).get(book_id)
        data_json = request.json

        book.name = data_json.get("name")
        book.year = data_json.get("year")

        db.session.add(book)
        db.session.commit()

        # book = Book.query.get_or_404(book_id)
        return book_schema.dump(book), 200
    
    def patch(self, book_id):
        book = db.session.query(Book).get(book_id)
        data_json = request.json

        if "name" in data_json:
            book.name = data_json.get("name")
        if "year" in data_json:
            book.year = data_json.get("year")

        db.session.add(book)
        db.session.commit()

        return book_schema.dump(book), 204

    def delete(self, book_id):
        """Удалить книгу по ID"""
        book = Book.query.get_or_404(book_id)
        db.session.delete(book)
        db.session.commit()
        return {"message": "Книга удалена"}, 204
    
    @authors_ns.route('/')
    class AuthorsView(Resource):
        def get(self):
            all_authors = db.session.query(Author).all()
            return authors_schema.dump(all_authors), 200
        
        def post(self):
            try:
                data_json = request.json
                new_author = Author(**data_json) # author_schema.load(data_json)
                db.session.add(new_author)
                db.session.commit()
                return author_schema.dump(new_author), 201
            except Exception as e:
                return f'Error {e}', 404
            
    @authors_ns.route('/<int:author_id>/')
    class AuthorView(Resource):
        def get(self, author_id):
            """Получить автора по ID"""
            author = Author.query.get_or_404(author_id)
            return author_schema.dump(author), 200
        
        def put(self, author_id):
            author = db.session.query(Author).get(author_id)
            data_json = request.json

            author.first_name = data_json.get('first_name')
            author.last_name = data_json.get('last_name')
            db.session.add(author)
            db.session.commit()

            return author_schema.dump(author), 204
        
        def patch (self, author_id):
            author = db.session.query(Author).get(author_id)
            data_json = request.json

            if 'first_name' in data_json:
                author.first_name = data_json.get('first_name')
            if 'last_name' in data_json:
                author.last_name = data_json.get('last_name')

            db.session.add(author)
            db.session.commit()
            return author_schema.dump(author), 204
        
        def delete (self, author_id):
            author = db.session.query(Author).get(author_id)

            db.session.delete(author)
            db.session.commit()

            return {"message": "Автор удалён"}, 204
        
if __name__ == '__main__':
    app.run (debug=False)


    
