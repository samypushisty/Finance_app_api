from api.api_v1.services.total_balance.interface import UserBalanceServiceI
from api.api_v1.services.total_balance.schemas import BalanceRead, BalancesHistoryRead
from api.api_v1.utils.repository import SQLAlchemyRepository
from api.api_v1.services.base_schemas.schemas import GenericResponse
from api.api_v1.utils.work_with_money import WorkWithMoneyRepository
from secure import JwtInfo
from typing import Callable
from sqlalchemy.ext.asyncio import AsyncSession

class UserBalanceService(UserBalanceServiceI):
    def __init__(self,
                 database_session:Callable[..., AsyncSession],
                 work_with_money: WorkWithMoneyRepository,
                 repository_balance:SQLAlchemyRepository,
                 settings_repository: SQLAlchemyRepository) -> None:
        self.session = database_session
        self.repository = repository_balance
        self.work_with_money = work_with_money
        self.repository_settings = settings_repository

    async def get_balances(self, token: JwtInfo) -> GenericResponse[BalancesHistoryRead]:
        async with self.session() as session:
            result = await self.repository.find(session=session,validate=True,chat_id=token.id)

        result = BalancesHistoryRead.model_validate(result, from_attributes=True)
        return GenericResponse[BalancesHistoryRead](detail=result)


    async def get_balance(self, token: JwtInfo) -> GenericResponse[BalanceRead]:
        async with self.session() as session:
            result = await self.repository.find(session=session, validate=True, chat_id=token.id)
            settings = await self.repository_settings.find(session=session, validate=True, chat_id=token.id)
        result.balance = await self.work_with_money.convert(base_currency=settings.main_currency,
                                                            convert_currency="RUB",
                                                            amount=result.balance)
        result = BalanceRead.model_validate(result, from_attributes=True)
        return GenericResponse[BalanceRead](detail=result)
