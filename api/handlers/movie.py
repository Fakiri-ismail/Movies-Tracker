import typing
import uuid
from collections import namedtuple
from functools import lru_cache

from fastapi import APIRouter, Body, Depends, Path, Query, Response
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse

from api.authentication import basic_authentication
from api.dto.movie import CreateMovieBody, UpdateMovieBody
from api.entities.movie import Movie
from api.repository.abstractions import MovieRepository, RepositoryException
from api.repository.movie_mongodb import MongoMovieRepository
from api.responses.movie import (DetailResponse, MovieCreatedResponse,
                                 MovieResponse)
from api.settings import Settings, settings_instance

router = APIRouter(
    prefix="/api/v1/movies",
    tags=["movies"],
    # Authentication
    dependencies=[Depends(basic_authentication)],
)


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


def pagination_params(skip: int = Query(0, ge=0), limit: int = Query(1000, le=1000)):
    Pagination = namedtuple("Pagination", ["skip", "limit"])
    return Pagination(skip=skip, limit=limit)


@router.post("/", status_code=201, response_model=MovieCreatedResponse)
async def post_create_movie(
    movie: CreateMovieBody = Body(..., title="Create Body"),
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
async def get_movie_by_id(
    movie_id: str,
    db: MovieRepository = Depends(movie_database),
    _=Depends(basic_authentication),
):
    movie = await db.get_by_id(movie_id)
    if not movie:
        return JSONResponse(
            status_code=404,
            content=jsonable_encoder(
                DetailResponse(message=f"Movie with id [{movie_id}] is not found.")
            ),
        )
    return MovieResponse(**movie.to_dict())


@router.get("/", response_model=typing.List[MovieResponse])
async def get_movie_by_title(
    title: str = Query(..., title="Movie Title", min_length=3),
    pagination=Depends(pagination_params),
    db: MovieRepository = Depends(movie_database),
):
    movies = await db.get_by_title(
        title=title, skip=pagination.skip, limit=pagination.limit
    )
    movies_return_value = []
    for movie in movies:
        movies_return_value.append(MovieResponse(**movie.to_dict()))
    return movies_return_value


@router.patch(
    "/{movie_id}",
    responses={200: {"model": DetailResponse}, 400: {"model": DetailResponse}},
)
async def patch_update_movie(
    movie_id: str = Path(..., title="Movie ID", description="ID of the movie."),
    update_param: UpdateMovieBody = Body(..., title="Update Body"),
    db: MovieRepository = Depends(movie_database),
):
    try:
        await db.update(
            movie_id=movie_id,
            update_param=update_param.dict(exclude_unset=True, exclude_none=True),
        )
        return DetailResponse(message=f"Movie updated.")
    except RepositoryException as e:
        return JSONResponse(
            status_code=400,
            content=jsonable_encoder(DetailResponse(message=str(e))),
        )


@router.delete("/{movie_id}", status_code=204)
async def delete_movie(movie_id: str, db: MovieRepository = Depends(movie_database)):
    await db.delete(movie_id=movie_id)
    return Response(status_code=204)
