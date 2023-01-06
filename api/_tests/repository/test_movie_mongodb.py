import asyncio
from asyncore import loop
import secrets
import pytest

from api.entities.movie import Movie
from api.repository.movie.abstractions import RepositoryException
from api.repository.movie.movie_mongodb import MongoMovieRepository


@pytest.fixture(scope="module")
def movie():
    return Movie(
        _id="movie1",
        title="365 Days",
        description="A woman falls victim to a dominant mafia boss, who imprisons her and gives her one year to fall in love with him",
        year=2020,
        watched=True,
    )


@pytest.fixture(scope="module")
def database():
    return MongoMovieRepository(database="test_movie_db")


@pytest.mark.asyncio
async def test_create(database, movie):
    await database.create(movie)
    assert await database.get_by_id(movie_id=movie.id) == movie
    await database.delete(movie.id)


@pytest.mark.parametrize("movie_id, excepted_movie", [("movie2", None)])
@pytest.mark.asyncio
async def test_get_by_id(database, movie, movie_id, excepted_movie):
    await database.create(movie)
    assert await database.get_by_id(movie_id) == excepted_movie
    await database.delete(movie.id)


@pytest.mark.asyncio
async def test_get_by_title(database, movie):
    await database.create(movie)
    assert await database.get_by_title(movie.title) == [movie]
    await database.delete(movie.id)


@pytest.mark.asyncio
async def test_update(database, movie):
    await database.create(movie)
    await database.update(
        movie_id="movie1", update_param={"year": 2023, "watched": False}
    )
    mv = await database.get_by_id("movie1")
    assert mv.year == 2023
    assert mv.watched == False
    await database.delete(movie.id)


@pytest.mark.asyncio
async def test_delete(database, movie):
    await database.create(movie)
    await database.delete(movie.id)
    assert await database.get_by_id("movie1") is None
