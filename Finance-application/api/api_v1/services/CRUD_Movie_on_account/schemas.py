from decimal import Decimal
from typing import  List, Optional
from core.redis_db.redis_helper import redis_client
from pydantic import BaseModel, Field, field_validator, model_validator, condecimal

from core.models.base import MovieType


class UserMoviePost(BaseModel):
    title: str = Field(max_length=15)
    description: Optional[str] = Field(None, max_length=256)
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
        if ((self.type == "earning" and (not self.earnings_id is None) and self.categories_id is None) or
                (self.type == "outlay" and (not self.categories_id is None) and self.earnings_id is None)):
            return self
        raise ValueError("should be one of categories_id and earnings_id")


    @field_validator("currency", mode="after")
    def validate_currency(cls, value):
        value = value.upper()
        if not redis_client.exists(value):
            raise ValueError(f"Currency '{value}' does not exist in Redis")
        return value


class UserMoviePatch(BaseModel):
    table_id: int = Field(ge=0)
    title: Optional[str] = Field(None, max_length=15)
    description: Optional[str] = Field(None, max_length=256)
    worth: Optional[Decimal] = Field(None,gt=0, decimal_places=2)
    currency: Optional[str] = Field(None,max_length=3)

    @field_validator("currency", mode="after")
    def validate_currency(cls, value):
        if value:
            value = value.upper()
            if not redis_client.exists(value):
                raise ValueError(f"Currency '{value}' does not exist in Redis")
        return value

class UserMovieGet(BaseModel):
    table_id: int = Field(ge=0)

class UserMoviesGet(BaseModel):
    page: int = Field(ge=1)
    earnings_id: Optional[int] = Field(None, ge=0)
    categories_id: Optional[int] = Field(None, ge=0)
    cash_account_id: Optional[int] = Field(None, ge=0)

    @model_validator(mode="after")
    def check_passwords_match(self) -> "UserMoviesGet":
        if not(self.earnings_id is not None and self.categories_id is not None):
            return self
        raise ValueError("should be one of categories_id and earnings_id")

class UserMovieRead(BaseModel):
    chat_id: int = Field(ge=10000000, le=10000000000)
    table_id: int  = Field(ge=0)
    title: str = Field(max_length=15)
    description: Optional[str] = Field(None, max_length=256)
    type: MovieType
    worth: Decimal = Field(gt=0, decimal_places=2)
    currency: Optional[str] = Field(max_length=3)
    cash_account: int
    categories_id: Optional[int]
    earnings_id: Optional[int]

    class Config:
        validate_assignment = True
        use_enum_values = True



class UserMoviesRead(BaseModel):
    movies: List[UserMovieRead]
