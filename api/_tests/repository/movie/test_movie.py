import pytest

from api.entities.movie import Movie
from api.repository.movie.abstractions import RepositoryException
from api.repository.movie.memory import MemoryMovieRepository


@pytest.fixture(scope="module")
def movie_1():
    return Movie(
        movie_id="movie1",
        title="365 Days",
        description="A woman falls victim to a dominant mafia boss, who imprisons her and gives her one year to fall in love with him",
        year=2020,
        watched=True,
    )


def test_create(movie_1):
    repo = MemoryMovieRepository()
    repo.create(movie_1)
    assert repo.get_by_id(movie_id="movie1") is movie_1


@pytest.mark.parametrize("movies, movie_id, excepted_movie", [([], "movie1", None)])
def test_get_by_id(movies, movie_id, excepted_movie):
    repo = MemoryMovieRepository()
    for movie in movies:
        repo.create(movie)
    assert repo.get_by_id(movie_id) == excepted_movie


@pytest.mark.parametrize("movies, movie_title, excepted_movies", [([], "365 Days", [])])
def test_get_by_title(movies, movie_title, excepted_movies):
    repo = MemoryMovieRepository()
    for movie in movies:
        repo.create(movie)
    assert repo.get_by_title(movie_title) == excepted_movies


def test_update(movie_1):
    repo = MemoryMovieRepository()
    repo.create(movie_1)
    repo.update(movie_id="movie1", update_param={"watched": False})
    assert repo.get_by_id("movie1").watched == False


def test_update_fail(movie_1):
    repo = MemoryMovieRepository()
    repo.create(movie_1)
    with pytest.raises(RepositoryException):
        repo.update(movie_id="movie1", update_param={"id": "movie2"})


def test_delete(movie_1):
    repo = MemoryMovieRepository()
    repo.create(movie_1)
    repo.delete("movie1")
    assert repo.get_by_id("movie1") is None
