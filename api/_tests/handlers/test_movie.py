import functools

import pytest
from starlette.testclient import TestClient

from api.api import creat_app
from api.entities.movie import Movie
from api.handlers.movie import movie_database
from api.repository.movie_memory import MemoryMovieRepository
from api.settings import Settings, settings_instance


def memory_repository_dependency(dependency):
    return dependency


@pytest.fixture()
def client():
    settings: Settings = settings_instance()
    settings.enable_metrics = False
    return TestClient(app=creat_app())


@pytest.mark.asyncio
async def test_post_create_movie(client):
    client.app.dependency_overrides[movie_database] = MemoryMovieRepository
    result = client.post(
        "/api/v1/movies/",
        json={
            "title": "Classe 8",
            "description": "Mjid et Miloud <3",
            "year": 2010,
            "watched": True,
        },
    )
    assert result.status_code == 201


@pytest.mark.asyncio
async def test_post_create_movie_validation_error(client):
    client.app.dependency_overrides[movie_database] = MemoryMovieRepository
    result = client.post(
        "/api/v1/movies/",
        json={
            "title": "Classe 8",
            "description": "Mjid et Miloud <3",
            # Year should be greater than 1900
            "year": 1800,
            "watched": True,
        },
    )
    assert result.status_code == 422


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "movies, movie_id, excepted_status_code, excepted_result",
    [
        ([], "88-66", 404, {"message": "Movie with id [88-66] is not found."}),
        (
            [
                Movie(
                    _id="88-09",
                    title="Classe 8",
                    description="Mjid et Miloud <3",
                    year=2010,
                    watched=True,
                )
            ],
            "88-09",
            200,
            {
                "title": "Classe 8",
                "description": "Mjid et Miloud <3",
                "year": 2010,
                "watched": True,
            },
        ),
    ],
)
async def test_get_movie_by_id(
    client, movies, movie_id, excepted_status_code, excepted_result
):
    repo = MemoryMovieRepository()
    patched_dependency = functools.partial(memory_repository_dependency, repo)
    client.app.dependency_overrides[movie_database] = patched_dependency
    for movie in movies:
        await repo.create(movie)
    result = client.get(f"/api/v1/movies/{movie_id}")
    assert result.status_code == excepted_status_code
    assert result.json() == excepted_result


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "movies, movie_title, excepted_status_code, excepted_result",
    [
        ([], "Elite", 200, []),
        (
            [
                Movie(
                    _id="88-09",
                    title="Classe 8",
                    description="Mjid et Miloud <3",
                    year=2010,
                    watched=True,
                ),
                Movie(
                    _id="77-65",
                    title="Elite",
                    description="Bla bla bla ...",
                    year=2020,
                    watched=False,
                ),
            ],
            "Elite",
            200,
            [
                {
                    "title": "Elite",
                    "description": "Bla bla bla ...",
                    "year": 2020,
                    "watched": False,
                }
            ],
        ),
    ],
)
async def test_get_movie_by_title(
    client, movies, movie_title, excepted_status_code, excepted_result
):
    repo = MemoryMovieRepository()
    patched_dependency = functools.partial(memory_repository_dependency, repo)
    client.app.dependency_overrides[movie_database] = patched_dependency
    for movie in movies:
        await repo.create(movie)
    result = client.get(f"/api/v1/movies/?title={movie_title}")
    assert result.status_code == excepted_status_code
    assert result.json() == excepted_result


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "movies, movie_id, update_params, excepted_status_code, excepted_result",
    [
        ([], "88-66", {}, 400, {"message": "movie 88-66 not found"}),
        (
            [
                Movie(
                    _id="88-09",
                    title="Classe 8",
                    description="Mjid et Miloud <3",
                    year=2010,
                    watched=True,
                )
            ],
            "88-09",
            {"year": 2010},
            200,
            {"message": "Movie updated."},
        ),
    ],
)
async def test_patch_update_movie(
    client, movies, movie_id, update_params, excepted_status_code, excepted_result
):
    repo = MemoryMovieRepository()
    patched_dependency = functools.partial(memory_repository_dependency, repo)
    client.app.dependency_overrides[movie_database] = patched_dependency
    for movie in movies:
        await repo.create(movie)
    result = client.patch(f"/api/v1/movies/{movie_id}", json=update_params)
    assert result.status_code == excepted_status_code
    assert result.json() == excepted_result


@pytest.mark.asyncio
async def test_delete_movie(client):
    repo = MemoryMovieRepository()
    patched_dependency = functools.partial(memory_repository_dependency, repo)
    client.app.dependency_overrides[movie_database] = patched_dependency
    await repo.create(
        Movie(
            _id="88-09",
            title="Classe 8",
            description="Mjid et Miloud <3",
            year=2010,
            watched=True,
        )
    )
    result = client.delete(f"/api/v1/movies/88-09")
    assert result.status_code == 204
    assert await repo.get_by_id(movie_id="88-09") is None
