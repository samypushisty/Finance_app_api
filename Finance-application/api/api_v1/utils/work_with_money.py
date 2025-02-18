from abc import ABC, abstractmethod
from decimal import Decimal, ROUND_HALF_UP
from typing import Callable, Literal
from redis.asyncio import Redis
from api.api_v1.services.base_schemas.schemas import StandartException

class AbstractConverter(ABC):
    @abstractmethod
    async  def convert(self, base_currency:str, convert_currency:str, amount:Decimal):
        ...

    @abstractmethod
    async def add_transaction(self, old_balance:Decimal, amount: Decimal,
                              type_operation: Literal["earning","outlay"]):
        ...

    @abstractmethod
    async def edit_transaction(self, old_balance: Decimal, old_amount: Decimal,
                               new_amount: Decimal, type_operation: str):
        ...

    @abstractmethod
    async def delete_transaction(self, old_balance: Decimal, amount: Decimal,
                              type_operation: Literal["earning", "outlay"]):
        ...


class WorkWithMoneyRepository(AbstractConverter):


    def __init__(self,db_redis: Callable[..., Redis]) -> None:
        self.db_redis = db_redis


    async def convert(self, base_currency:str, convert_currency:str, amount:Decimal):
        async with self.db_redis() as session:
            if base_currency == convert_currency:
                return amount
            price_base  = Decimal(await session.get(base_currency))
            price_convert = Decimal(await session.get(convert_currency))
        answer = (amount/price_convert*price_base).quantize(
                Decimal("0.00"),
                rounding=ROUND_HALF_UP)
        return answer

    async def add_transaction(self, old_balance: Decimal, amount: Decimal,
                              type_operation: str):
        if type_operation == "outlay":
            old_balance -= amount
            if old_balance < 0:
                raise StandartException(status_code=403, detail="balance < 0")
        elif type_operation == "earning":
            old_balance += amount
        return old_balance

    async def edit_transaction(self, old_balance: Decimal, old_amount: Decimal,
                              new_amount: Decimal, type_operation: str):
        if type_operation == "earning":
            old_balance -= old_amount
            old_balance += new_amount
        elif type_operation == "outlay":
            old_balance += old_amount
            old_balance -= new_amount
        if old_balance < 0:
            raise StandartException(status_code=403, detail="balance < 0")
        return old_balance

    async def delete_transaction(self, old_balance: Decimal, amount: Decimal,
                              type_operation: str):
        if type_operation == "earning":
            old_balance -= amount
            if old_balance < 0:
                raise StandartException(status_code=403, detail="balance < 0")
        elif type_operation == "outlay":
            old_balance += amount
        return old_balance
