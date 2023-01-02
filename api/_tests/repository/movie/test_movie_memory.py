import pytest

from api.entities.movie import Movie
from api.repository.movie.abstractions import RepositoryException
from api.repository.movie.movie_memory import MemoryMovieRepository

@pytest.fixture()
def repo():
    return MemoryMovieRepository()


@pytest.fixture()
def movie():
    return Movie(
        _id="movie1",
        title="365 Days",
        description="A woman falls victim to a dominant mafia boss, who imprisons her and gives her one year to fall in love with him",
        year=2020,
        watched=True,
    )


@pytest.mark.asyncio
async def test_create(repo, movie):
    repo = MemoryMovieRepository()
    await repo.create(movie)
    assert await repo.get_by_id(movie_id="movie1") == movie


@pytest.mark.parametrize("movies, movie_id, excepted_movie", [([], "movie1", None)])
@pytest.mark.asyncio
async def test_get_by_id(repo, movies, movie_id, excepted_movie):
    for movie in movies:
        await repo.create(movie)
    assert await repo.get_by_id(movie_id) == excepted_movie


@pytest.mark.parametrize("movies, movie_title, excepted_movies", [([], "365 Days", [])])
@pytest.mark.asyncio
async def test_get_by_title(repo, movies, movie_title, excepted_movies):
    for movie in movies:
        await repo.create(movie)
    assert await repo.get_by_title(movie_title) == excepted_movies


@pytest.mark.asyncio
async def test_update(repo, movie):
    await repo.create(movie)
    await repo.update(movie_id="movie1", update_param={"watched": False})
    mv = await repo.get_by_id("movie1")
    assert mv.watched == False


@pytest.mark.asyncio
async def test_update_fail(repo, movie):
    await repo.create(movie)
    with pytest.raises(RepositoryException):
        await repo.update(movie_id="movie1", update_param={"id": "movie2"})


@pytest.mark.asyncio
async def test_delete(repo, movie):
    await repo.create(movie)
    await repo.delete("movie1")
    assert await repo.get_by_id("movie1") is None
