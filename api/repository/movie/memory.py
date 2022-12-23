import typing
from api.entities.movie import Movie
from api.repository.movie.abstractions import MovieRepository, RepositoryException


class MemoryMovieRepository(MovieRepository):
    def __init__(self):
        self._storage = {}

    def create(self, movie: Movie):
        self._storage[movie.id] = movie

    def get_by_id(self, movie_id: str) -> typing.Optional[Movie]:
        return self._storage.get(movie_id)

    def get_by_title(self, title: str) -> typing.List[Movie]:
        movies = [movie for _, movie in self._storage.items() if movie.title == title]
        return movies

    def update(self, movie_id: str, update_param: dict):
        movie = self._storage.get(movie_id)
        if movie:
            for key, value in update_param.items():
                if key == "id" and value != movie_id:
                    raise RepositoryException("can't update movie id")
                # Ensure that user doesn't add keys that don't exist on movie entity.
                if hasattr(movie, key):
                    movie[key] = value
            self._storage[movie_id] = movie
        raise RepositoryException(f"movie {movie_id} not found")

    def delete(self, movie_id: str):
        self._storage.pop(movie_id, None)
