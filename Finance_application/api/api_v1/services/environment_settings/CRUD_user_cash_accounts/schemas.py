from typing import List, Optional

from pydantic import BaseModel, Field, field_validator, condecimal
from decimal import Decimal

from api.api_v1.services.base_schemas.schemas import StandartException
from core.models.base import CashAccountType
from core.redis_db.redis_helper import redis_client


class UserCashAccountPost(BaseModel):
    balance: Decimal = Field(ge=0, decimal_places=2)
    name: str = Field(max_length=15)
    description: Optional[str] = Field(None, max_length=256)
    type: CashAccountType
    currency: str = Field(max_length=3)

    class Config:
        use_enum_values = True

    @field_validator("currency", mode="after")
    def validate_currency(cls, value: str):
        value = value.upper()
        if not redis_client.exists(value):
            raise ValueError(f"Currency '{value}' does not exist in Redis")
        return value


class UserCashAccountPatch(BaseModel):
    table_id: int
    name: Optional[str] = Field(None, max_length=15)
    description: Optional[str] = Field(None, max_length=256)
    currency: Optional[str] = Field(None, max_length=3)

    @field_validator("currency", mode="after")
    def validate_currency(cls, value: str):
        value = value.upper()
        if not redis_client.exists(value):
            raise ValueError(f"Currency '{value}' does not exist in Redis")
        return value

class UserCashAccountGet(BaseModel):
    table_id: int
    currency: Optional[str]  = Field(None, max_length=3)

    @field_validator("currency", mode="after")
    def validate_currency(cls, value: str):
        if value is None:
            return value
        value = value.upper()
        if not redis_client.exists(value):
            raise StandartException(status_code=401, detail=f"Currency '{value}' does not exist in Redis")
        return value


class UserCashAccountRead(BaseModel):
    table_id: int
    chat_id: int = Field(ge=10000000, le=10000000000)
    balance: Decimal = Field(decimal_places=2)
    name: str = Field(max_length=15)
    description: Optional[str] = Field(None, max_length=256)
    type: CashAccountType
    currency: str = Field(max_length=3)

    class Config:
        validate_assignment = True
        use_enum_values = True



class UserCashAccountsRead(BaseModel):
    accounts: List[UserCashAccountRead]
