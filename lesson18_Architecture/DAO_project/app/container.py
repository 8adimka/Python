from app.dao.directors import DirectorDAO
from app.dao.genres import GenreDAO
from app.dao.movies import MovieDAO
from app.database import db
from app.services.directors import DirectorService
from app.services.genres import GenreService
from app.services.movies import MovieService

movie_dao = MovieDAO(db.session)
movie_service = MovieService(movie_dao)

genre_dao = GenreDAO(db.session)
genre_service = GenreService(genre_dao)

director_dao = DirectorDAO(db.session)
director_service = DirectorService(director_dao)
