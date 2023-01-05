from pydantic import BaseModel


class DetailResponse(BaseModel):
    message: str


class MovieCreatedResponse(BaseModel):
    _id: str


class MovieResponse(MovieCreatedResponse):
    title: str
    description: str
    year: int
    watched: bool
