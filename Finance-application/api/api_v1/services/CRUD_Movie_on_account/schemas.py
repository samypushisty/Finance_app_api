from decimal import Decimal
from typing import  List, Optional
from core.redis_db.redis_helper import redis_client
from pydantic import BaseModel, Field, field_validator, model_validator, condecimal

from core.models.base import MovieType


class UserMoviePost(BaseModel):
    title: str = Field(max_length=15)
    description: str = Field(max_length=256)
    type: MovieType
    worth: Decimal = Field(gt=0, decimal_places=2)
    currency: str = Field(max_length=3)
    cash_account: int
    categories_id: Optional[int] = None
    earnings_id: Optional[int] = None

    class Config:
        use_enum_values = True

    @model_validator(mode="after")
    def check_passwords_match(self) -> "UserMoviePost":
        if (not self.categories_id is None) and (not self.earnings_id is None) or (self.categories_id is None and self.earnings_id is None):
            raise ValueError("should be one of categories_id and earnings_id")
        return self

    @field_validator("currency", mode="after")
    def validate_type(cls, value):
        if not redis_client.exists(value):
            raise ValueError(f"Currency '{value}' does not exist in Redis")
        return value


class UserMoviePatch(BaseModel):
    movie_id: int
    title: str = Field(max_length=15)
    description: str = Field(max_length=256)
    type: MovieType

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
    worth: Decimal = Field(gt=0, decimal_places=2)
    cash_account: int
    categories_id: Optional[int]
    earnings_id: Optional[int]

    class Config:
        validate_assignment = True
        use_enum_values = True

    @field_validator("type", mode="before")
    def validate_currency(cls, value: str):
        value = value.upper()
        if isinstance(value, MovieType):
            return MovieType(value).value
        return value


class UserMoviesRead(BaseModel):
    movies: List[UserMovieRead]
