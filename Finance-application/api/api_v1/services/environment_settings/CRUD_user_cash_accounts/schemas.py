from typing import  List

from pydantic import BaseModel, Field, field_validator, condecimal
from decimal import Decimal
from core.models.base import CashAccountType
from core.redis_db.redis_helper import redis_client


class UserCashAccountPost(BaseModel):
    balance: Decimal = Field(gt=0, decimal_places=2)
    name: str = Field(max_length=15)
    description: str = Field(max_length=256)
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
    cash_id: int
    name: str = Field(max_length=15)
    description: str = Field(max_length=256)

class UserCashAccountGet(BaseModel):
    cash_id: int


class UserCashAccountRead(BaseModel):
    cash_id: int
    chat_id: int = Field(ge=10000000, le=10000000000)
    balance: Decimal = Field(gt=0, decimal_places=2)
    name: str = Field(max_length=15)
    description: str = Field(max_length=256)
    type: CashAccountType
    currency: str = Field(max_length=3)

    class Config:
        validate_assignment = True
        use_enum_values = True

    @field_validator('type', mode='before')
    def validate_type(cls, value):
        if isinstance(value, CashAccountType):
            return CashAccountType(value).value
        return value


class UserCashAccountsRead(BaseModel):
    accounts: List[UserCashAccountRead]
