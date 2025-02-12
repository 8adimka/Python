from app.dao.movies import MovieDAO


class MovieService:
    def __init__(self, dao: MovieDAO):
        self.dao = dao

    def get_one(self, movie_id):
        return self.dao.get_one(movie_id)
    
    def get_all(self, director_id = None, genre_id = None):
        """Filtration logic"""
        filters = {}
        if director_id is not None:
            filters["director_id"] = director_id
        if genre_id is not None:
            filters["genre_id"] = genre_id

        if filters:
            return self.dao.filter_by(**filters)
        return self.dao.get_all()

    def create (self, data):
        return self.dao.create(data)

    def update (self, data):
        movie_id = data.get("id")
        movie = self.dao.get_one(movie_id)

        movie.title = data.get("title")
        movie.description = data.get("description")
        movie.trailer = data.get("trailer")
        movie.year = data.get("year")
        movie.rating = data.get("rating")

        self.dao.update(movie)

    def update_partial(self, data):
        movie_id = data.get("id")
        movie = self.dao.get_one(movie_id)
        if "title" in data:
            movie.title = data.get("title")
        if "description" in data:
            movie.description = data.get("description")
        if "trailer" in data:
            movie.trailer = data.get("trailer")
        if "year" in data:
            movie.year = data.get("year")
        if "rating" in data:
            movie.rating = data.get("rating")

        self.dao.update(movie)

    def delete(self, movie_id):
        self.dao.delete(movie_id)
