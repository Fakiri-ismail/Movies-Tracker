import abc
import typing

from api.entities.movie import Movie


class RepositoryException(Exception):
    pass


class MovieRepository(abc.ABC):
    async def create(self, movie: Movie):
        """
        INsert a movie to the database and return True on success.
        Raises RepositoryException if failure.
        """
        raise NotImplementedError

    async def get_by_id(self, movie_id: str) -> typing.Optional[Movie]:
        """
        Retrieves a movie by his ID and if it's not found return None.
        """
        raise NotImplementedError

    async def get_by_title(
        self, title: str, skip: int = 0, limit: int = 1000
    ) -> typing.List[Movie]:
        """
        Return a list of movies wich share the same title.
        """
        raise NotImplementedError

    async def update(self, movie_id: str, update_param: dict):
        """
        Update a movie by his ID.
        """
        raise NotImplementedError

    async def delete(self, movie_id: str):
        """
        Delete a movie by his ID.
        Raises RepositoryException if failure.
        """
        raise NotImplementedError
