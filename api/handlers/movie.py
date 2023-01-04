from functools import lru_cache
import uuid
from fastapi import APIRouter, Body, Depends
from api.dto.movie import CreateMovieBody
from api.entities.movie import Movie
from api.repository.movie.abstractions import MovieRepository
from api.repository.movie.movie_mongodb import MongoMovieRepository

from api.responses.movie import MovieCreatedResponse
from api.settings import Settings


router = APIRouter(prefix="/api/v1/movies", tags=["movies"])


@lru_cache()
def settings():
    return Settings()


def movie_database(settings: Settings = Depends(settings)):
    return MongoMovieRepository(
        connection_string=settings.mongo_connection_string,
        database=settings.mongo_database_name,
    )


@router.post("/", status_code=201, response_model=MovieCreatedResponse)
async def create_movie(
    movie: CreateMovieBody = Body(
        ..., title="Movie name", description="The movie details"
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
    return MovieCreatedResponse(movie_id=_id)
