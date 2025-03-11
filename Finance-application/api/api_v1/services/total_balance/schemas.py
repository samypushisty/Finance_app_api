from decimal import Decimal
from pydantic import BaseModel, Field



class BalanceRead(BaseModel):
    chat_id: int = Field(ge=10000000, le=10000000000)
    balance: Decimal



class BalancesHistoryRead(BaseModel):
    balances_history: list
