from decimal import Decimal
from typing import  Optional
from core.redis_db.redis_helper import redis_client
from pydantic import BaseModel, Field, field_validator


class BalanceRead(BaseModel):
    chat_id: int = Field(ge=10000000, le=10000000000)
    balance: Decimal

class BalanceGet(BaseModel):
    currency: Optional[str] = Field(None, max_length=3)

    @field_validator("currency", mode="after")
    def validate_currency(cls, value):
        if value:
            value = value.upper()
            if not redis_client.exists(value):
                raise ValueError(f"Currency '{value}' does not exist in Redis")
        return value

class BalancesHistoryRead(BaseModel):
    balances_history: list
