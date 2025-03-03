from abc import abstractmethod
from typing import Protocol
from api.api_v1.services.total_balance.schemas import BalanceRead, BalancesHistoryRead
from secure import JwtInfo
from api.api_v1.services.base_schemas.schemas import GenericResponse

class UserBalanceServiceI(Protocol):

    @abstractmethod
    async def get_balance(self, token: JwtInfo) -> GenericResponse[BalanceRead]:
        ...

    @abstractmethod
    async def get_balances(self, token: JwtInfo) -> GenericResponse[BalancesHistoryRead]:
        ...
