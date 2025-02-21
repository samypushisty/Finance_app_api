from typing import List, Optional
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
    earning_id: Optional[int] = None
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
    earning_id: int


class UserTypeEarningsRead(BaseModel):
    earning_id: int
    chat_id: int = Field(ge=10000000, le=10000000000)
    name: str = Field(max_length=15)
    description: str = Field(max_length=15)
    currency: str = Field(max_length=3)


class UserTypesEarningsRead(BaseModel):
    types_of_earnings: List[UserTypeEarningsRead]
