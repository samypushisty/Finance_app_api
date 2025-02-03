from typing import  List

from pydantic import BaseModel, Field, field_validator

from core.models.base import CashAccountType


class UserCashAccountPost(BaseModel):
    balance: float = Field(ge=0)
    name: str = Field(max_length=15)
    description: str = Field(max_length=256)
    type: CashAccountType
    currency: str = Field(max_length=3)

    class Config:
        use_enum_values = True

class UserCashAccountPatch(BaseModel):
    cash_id: int
    name: str = Field(max_length=15)
    description: str = Field(max_length=256)
    type: CashAccountType
    currency: str = Field(max_length=3)

    class Config:
        use_enum_values = True

class UserCashAccountGet(BaseModel):
    cash_id: int


class UserCashAccountRead(BaseModel):
    cash_id: int
    chat_id: int = Field(ge=10000000, le=10000000000)
    balance: float = Field(ge=0)
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
