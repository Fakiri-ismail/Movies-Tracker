import pytest

from api.entities.movie import Movie
from api.repository.movie.abstractions import RepositoryException
from api.repository.movie.movie_memory import MemoryMovieRepository


@pytest.fixture(scope="module")
def movie_1():
    return Movie(
        _id="movie1",
        title="365 Days",
        description="A woman falls victim to a dominant mafia boss, who imprisons her and gives her one year to fall in love with him",
        year=2020,
        watched=True,
    )


@pytest.mark.asyncio
async def test_create(movie_1):
    repo = MemoryMovieRepository()
    await repo.create(movie_1)
    assert await repo.get_by_id(movie_id="movie1") is movie_1


@pytest.mark.parametrize("movies, movie_id, excepted_movie", [([], "movie1", None)])
@pytest.mark.asyncio
async def test_get_by_id(movies, movie_id, excepted_movie):
    repo = MemoryMovieRepository()
    for movie in movies:
        await repo.create(movie)
    assert await repo.get_by_id(movie_id) == excepted_movie


@pytest.mark.parametrize("movies, movie_title, excepted_movies", [([], "365 Days", [])])
@pytest.mark.asyncio
async def test_get_by_title(movies, movie_title, excepted_movies):
    repo = MemoryMovieRepository()
    for movie in movies:
        await repo.create(movie)
    assert await repo.get_by_title(movie_title) == excepted_movies


@pytest.mark.asyncio
async def test_update(movie_1):
    repo = MemoryMovieRepository()
    await repo.create(movie_1)
    await repo.update(movie_id="movie1", update_param={"watched": False})
    movie = await repo.get_by_id("movie1")
    assert movie.watched == False


@pytest.mark.asyncio
async def test_update_fail(movie_1):
    repo = MemoryMovieRepository()
    await repo.create(movie_1)
    with pytest.raises(RepositoryException):
        await repo.update(movie_id="movie1", update_param={"id": "movie2"})


@pytest.mark.asyncio
async def test_delete(movie_1):
    repo = MemoryMovieRepository()
    await repo.create(movie_1)
    await repo.delete("movie1")
    assert await repo.get_by_id("movie1") is None
