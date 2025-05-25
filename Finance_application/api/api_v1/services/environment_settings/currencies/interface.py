from abc import abstractmethod
from typing import Protocol
from .schemas import CurrencyGet, CurrenciesRead, CurrencyRead
from api.api_v1.services.base_schemas.schemas import GenericResponse

class UserCurrenciesServiceI(Protocol):

    @abstractmethod
    async def get_currencies(self) -> GenericResponse[CurrenciesRead]:
        ...

    @abstractmethod
    async def get_currency_price(self,name_currency: CurrencyGet) -> GenericResponse[CurrencyRead]:
        ...


