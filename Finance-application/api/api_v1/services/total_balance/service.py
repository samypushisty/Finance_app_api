from api.api_v1.services.total_balance.interface import UserBalanceServiceI
from api.api_v1.services.total_balance.schemas import BalanceRead, BalancesHistoryRead
from api.api_v1.utils.repository import SQLAlchemyRepository
from api.api_v1.services.base_schemas.schemas import GenericResponse
from secure import JwtInfo
from typing import Callable
from sqlalchemy.ext.asyncio import AsyncSession

class UserBalanceService(UserBalanceServiceI):
    def __init__(self,
                 database_session:Callable[..., AsyncSession],
                 repository_balance:SQLAlchemyRepository) -> None:
        self.session = database_session
        self.repository = repository_balance

    async def get_balances(self, token: JwtInfo) -> GenericResponse[BalancesHistoryRead]:
        async with self.session() as session:
            result = await self.repository.find(session=session,chat_id=token.id)
        result = BalancesHistoryRead.model_validate(result, from_attributes=True)
        return GenericResponse[BalancesHistoryRead](detail=result)


    async def get_balance(self, token: JwtInfo) -> GenericResponse[BalanceRead]:
        async with self.session() as session:
            result = await self.repository.find(session=session, chat_id=token.id)
        result = BalanceRead.model_validate(result, from_attributes=True)
        return GenericResponse[BalanceRead](detail=result)
