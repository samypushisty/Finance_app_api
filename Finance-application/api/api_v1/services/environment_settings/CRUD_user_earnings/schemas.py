from decimal import Decimal
from typing import List, Optional

from api.api_v1.services.base_schemas.schemas import StandartException
from core.redis_db.redis_helper import redis_client
from pydantic import BaseModel, Field, field_validator



class UserTypeEarningsPost(BaseModel):
    name: str = Field(max_length=15)
    description: str = Field(max_length=256)
    currency: str = Field(max_length=3)

    @field_validator("currency", mode="after")
    def validate_currency(cls, value: str):
        value = value.upper()
        if not redis_client.exists(value):
            raise ValueError(f"Currency '{value}' does not exist in Redis")
        return value


class UserTypeEarningsPatch(BaseModel):
    table_id: Optional[int] = None
    name: Optional[str] = Field(None, max_length=15)
    description: Optional[str] = Field(None, max_length=256)
    currency: Optional[str] = Field(None, max_length=3)

    @field_validator("currency", mode="after")
    def validate_currency(cls, value: str):
        value = value.upper()
        if not redis_client.exists(value):
            raise ValueError(f"Currency '{value}' does not exist in Redis")
        return value

class UserTypeEarningsGet(BaseModel):
    table_id: int
    currency: Optional[str] = Field(None, max_length=3)

    @field_validator("currency", mode="after")
    def validate_currency(cls, value: str):
        if value is None:
            return value
        value = value.upper()
        if not redis_client.exists(value):
            raise StandartException(status_code=401, detail=f"Currency '{value}' does not exist in Redis")
        return value


class UserTypeEarningsRead(BaseModel):
    table_id: int
    chat_id: int = Field(ge=10000000, le=10000000000)
    name: str = Field(max_length=15)
    description: str = Field(max_length=15)
    currency: str = Field(max_length=3)
    balance: Decimal = Field(decimal_places=2)


class UserTypesEarningsRead(BaseModel):
    types_of_earnings: List[UserTypeEarningsRead]
