import typing

from pydantic import BaseModel, validator


class CreateMovieBody(BaseModel):
    """
    CreateMovieBody is used as the body for the create movie endpoint.
    """

    title: str
    description: str
    year: int
    watched: bool = False

    @validator("title")
    def title_length_gt_three(cls, v):
        if len(v) <= 3:
            raise ValueError("Title's length must be greater than 4 characters")
        return v

    @validator("description")
    def description_words_gt_two(cls, v):
        if len(v.split(" ")) <= 2:
            raise ValueError("The description must contain at least 3 words")
        return v

    @validator("year")
    def year_gt_1900(cls, v):
        if v <= 1900:
            raise ValueError("The year must be greater than 1900")
        return v


class UpdateMovieBody(BaseModel):

    title: typing.Union[str, None] = None
    description: typing.Union[str, None] = None
    year: typing.Union[int, None] = None
    watched: typing.Union[bool, None] = False
