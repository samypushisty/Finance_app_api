from decimal import Decimal
from typing import  List, Optional

from pydantic import BaseModel, Field, field_validator, model_validator

from core.models.base import MovieType


class UserMoviePost(BaseModel):
    title: str = Field(max_length=15)
    description: str = Field(max_length=256)
    type: MovieType
    worth: Decimal
    cash_account: int
    categories_id: Optional[int] = None
    earnings_id: Optional[int] = None

    class Config:
        use_enum_values = True

    @model_validator(mode="after")
    def check_passwords_match(self) -> "UserMoviePost":
        if self.categories_id and self.earnings_id:
            raise ValueError("should be one of categories_id and earnings_id")
        return self


class UserMoviePatch(BaseModel):
    movie_id: int
    title: str = Field(max_length=15)
    description: str = Field(max_length=256)
    type: MovieType
    worth: Decimal
    cash_account: int
    categories_id: Optional[int] = None
    earnings_id: Optional[int] = None

    class Config:
        use_enum_values = True

    @model_validator(mode="after")
    def check_passwords_match(self) -> "UserMoviePatch":
        if self.categories_id and self.earnings_id:
            raise ValueError("should be one of categories_id and earnings_id")
        return self


class UserMovieGet(BaseModel):
    movie_id: int


class UserMovieRead(BaseModel):
    chat_id: int = Field(ge=10000000, le=10000000000)
    movie_id: int
    title: str = Field(max_length=15)
    description: str = Field(max_length=256)
    type: MovieType
    worth: Decimal
    cash_account: int
    categories_id: Optional[int]
    earnings_id: Optional[int]

    class Config:
        validate_assignment = True
        use_enum_values = True

    @field_validator("type", mode="before")
    def validate_type(cls, value):
        if isinstance(value, MovieType):
            return MovieType(value).value
        return value


class UserMoviesRead(BaseModel):
    movies: List[UserMovieRead]
