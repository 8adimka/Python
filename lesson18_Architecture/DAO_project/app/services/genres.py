from app.dao.genres import GenreDAO


class GenreService:
    def __init__(self, dao: GenreDAO):
        self.dao = dao

    def get_one(self, genre_id):
        return self.dao.get_one(genre_id)
    
    def get_all(self):
        return self.dao.get_all()

    def create (self, data):
        return self.dao.create(data)

    def update (self, data):
        genre_id = data.get("id")
        genre = self.dao.get_one(genre_id)

        genre.name = data.get("name")
        self.dao.update(genre)

    def update_partial(self, data):
        genre_id = data.get("id")
        genre = self.get_one(genre_id)
        if "name" in data:
            genre.name = data.get("name")

        self.dao.update(genre)

    def delete(self, genre_id):
        self.dao.delete(genre_id)


