from pydantic import BaseSettings, Field
from functools import lru_cache


class Settings(BaseSettings):
    # MongoDB Settings
    mongo_connection_string: str = Field(
        "mongodb://localhost:27017",
        title="MongoDB connection String",
        env="MONGODB_CONNECTION_STRING",
    )
    mongo_database_name: str = Field(
        "movie_track_db",
        title="MongoDB Movies Database Name",
        env="MONGODB_DATABASE_NAME",
    )


@lru_cache()
def settings_instance():
    """
    Settings instance to used as a FastAPI dependency.
    """
    return Settings()
