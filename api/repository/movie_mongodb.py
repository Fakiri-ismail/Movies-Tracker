import typing

import motor.motor_asyncio

from api.entities.movie import Movie
from api.repository.abstractions import MovieRepository, RepositoryException


class MongoMovieRepository(MovieRepository):
    """
    MemoryMovieRepository implements the reposetory pattern by using MongoDB.
    """

    def __init__(
        self,
        database: str = "movie_track_db",
        connection_string: str = "mongodb://localhost:27017",
    ):
        self._client = motor.motor_asyncio.AsyncIOMotorClient(connection_string)
        self._database = self._client[database]
        # Movie Collection
        self._movies = self._database["movies"]

    async def create(self, movie: Movie):
        await self._movies.insert_one(movie.to_dict())

    async def get_by_id(self, movie_id: str) -> typing.Optional[Movie]:
        document = await self._movies.find_one({"_id": movie_id})
        if document:
            return Movie(**document)
        return None

    async def get_by_title(self, title: str) -> typing.List[Movie]:
        movie_list: typing.List[Movie] = []
        documents_cursor = self._movies.find({"title": title})
        async for document in documents_cursor:
            movie_list.append(Movie(**document))
        return movie_list

    async def update(self, movie_id: str, update_param: dict):
        result = await self._movies.find_one({"_id": movie_id})
        if result:
            if "_id" in update_param:
                raise RepositoryException("can't update movie id")
            await self._movies.update_one({"_id": movie_id}, {"$set": update_param})
        else:
            raise RepositoryException(f"movie {movie_id} not found")

    async def delete(self, movie_id: str):
        await self._movies.delete_one({"_id": movie_id})
