from abc import ABC, abstractmethod
from decimal import Decimal, ROUND_HALF_UP
from typing import Callable
from redis.asyncio import Redis


class AbstractConverter(ABC):
    @abstractmethod
    async  def convert(self, base_currency:str, convert_currency:str, amount:Decimal):
        ...


class ConverterRepository(AbstractConverter):


    def __init__(self,db_redis: Callable[..., Redis]) -> None:
        self.db_redis = db_redis


    async def convert(self, base_currency:str, convert_currency:str, amount:Decimal):
        async with self.db_redis() as session:
            print(base_currency)
            price_base  = Decimal(await session.get(base_currency))
            price_convert = Decimal(await session.get(convert_currency))
        answer = (amount/price_convert*price_base).quantize(
                Decimal("0.00"),
                rounding=ROUND_HALF_UP)
        print(answer)
        print(type(answer))
        return answer