from api.api_v1.services.environment_settings.currencies.interface import UserCurrenciesServiceI
from api.api_v1.services.environment_settings.currencies.schemas import CurrenciesRead, CurrencyGet, CurrencyRead
from api.api_v1.services.base_schemas.schemas import GenericResponse, StandartException
from typing import Callable
from redis.asyncio import Redis
from sqlalchemy.ext.asyncio import AsyncSession


class UserCurrenciesService(UserCurrenciesServiceI):
    def __init__(self,db_redis: Callable[..., Redis], database_session:Callable[..., AsyncSession]) -> None:
        self.db_redis = db_redis
        self.session = database_session


    async def get_currencies(self) -> GenericResponse[CurrenciesRead]:
        async with self.db_redis() as session:
            result = await session.keys('*')
        if not result:
            raise StandartException(status_code=404, detail="currencies not found")
        result_currencies = CurrenciesRead(currencies=result)
        return GenericResponse[CurrenciesRead](detail=result_currencies)

    async def get_currency_price(self, name_currency: CurrencyGet) -> GenericResponse[CurrencyRead]:
        async with self.db_redis() as session:
            price  = float(await session.get(name_currency.name))
        if not price:
            raise StandartException(status_code=404, detail="currency not found")
        result_currency = CurrencyRead(name=name_currency.name,price=price)
        return GenericResponse[CurrencyRead](detail=result_currency)

