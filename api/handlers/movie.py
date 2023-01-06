import typing
import uuid
from functools import lru_cache

from fastapi import APIRouter, Body, Depends, Path, Query, Response

from api.dto.movie import CreateMovieBody, UpdateMovieBody
from api.entities.movie import Movie
from api.repository.abstractions import MovieRepository, RepositoryException
from api.repository.movie_mongodb import MongoMovieRepository
from api.responses.movie import (DetailResponse, MovieCreatedResponse,
                                 MovieResponse)
from api.settings import Settings, settings_instance

router = APIRouter(prefix="/api/v1/movies", tags=["movies"])


def _make_movie_database(settings: Settings) -> MovieRepository:
    return MongoMovieRepository(
        connection_string=settings.mongo_connection_string,
        database=settings.mongo_database_name,
    )


def movie_database(settings: Settings = Depends(settings_instance)):
    """
    Movie Repository instance to used as a FastAPI dependency.
    """

    @lru_cache()
    def cache():
        return _make_movie_database(settings)

    return cache()


@router.post("/", status_code=201, response_model=MovieCreatedResponse)
async def post_create_movie(
    movie: CreateMovieBody = Body(
        ..., title="Create Body", description="The movie details"
    ),
    db: MovieRepository = Depends(movie_database),
):
    """
    Create a movie.
    """
    # Generate movie ID
    _id = str(uuid.uuid4())
    await db.create(
        Movie(
            _id=_id,
            title=movie.title,
            description=movie.description,
            year=movie.year,
            watched=movie.watched,
        )
    )
    return MovieCreatedResponse(_id=_id)


@router.get(
    "/{movie_id}",
    responses={200: {"model": MovieResponse}, 404: {"model": DetailResponse}},
)
async def get_movie_by_id(movie_id: str, db: MovieRepository = Depends(movie_database)):
    movie = await db.get_by_id(movie_id)
    if not movie:
        return DetailResponse(message=f"Movie with [id = {movie_id}] is not found.")
    return MovieResponse(**movie.to_dict())


@router.get("/", response_model=typing.List[MovieResponse])
async def get_movie_by_title(
    title: str = Query(
        ..., title="Title", description="The title of movie", min_length=3
    ),
    db: MovieRepository = Depends(movie_database),
):
    movies = await db.get_by_title(title=title)
    movies_return_value = []
    for movie in movies:
        movies_return_value.append(MovieResponse(**movie.to_dict()))
    return movies_return_value


@router.patch(
    "/{movie_id}",
    responses={200: {"model": DetailResponse}, 404: {"model": DetailResponse}},
)
async def patch_update_movie(
    movie_id: str = Path(..., title="Movie ID", description="ID of the movie."),
    update_param: UpdateMovieBody = Body(
        ..., title="Update Body", description="Parameters of the movie to be updated."
    ),
    db: MovieRepository = Depends(movie_database),
):
    try:
        await db.update(
            movie_id=movie_id,
            update_param=update_param.dict(exclude_unset=True, exclude_none=True),
        )
        return DetailResponse(message=f"Movie updated.")
    except RepositoryException as e:
        return DetailResponse(message=str(e))


@router.delete("/{movie_id}", status_code=204)
async def patch_update_movie(
    movie_id: str, db: MovieRepository = Depends(movie_database)
):
    await db.delete(movie_id=movie_id)
    return Response(status_code=204)
