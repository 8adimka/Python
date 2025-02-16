from app.database import db
from app.dao.genres import GenreDAO
from app.dao.movies import MovieDAO
from app.dao.users import UserDAO
from app.dao.directors import DirectorDAO
from app.services.movies import MovieService
from app.services.genres import GenreService
from app.services.users import UserService
from app.services.directors import DirectorService



movie_dao = MovieDAO(db.session)
movie_service = MovieService(movie_dao)

genre_dao = GenreDAO(db.session)
genre_service = GenreService(genre_dao)

director_dao = DirectorDAO(db.session)
director_service = DirectorService(director_dao)

user_dao = UserDAO(db.session)
user_service = UserService(user_dao)
