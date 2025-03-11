from decimal import Decimal, ROUND_HALF_UP

from redis import Redis

from api.api_v1.services.total_balance.interface import UserBalanceServiceI
from api.api_v1.services.total_balance.schemas import BalanceRead, BalancesHistoryRead
from api.api_v1.utils.repository import SQLAlchemyRepository
from api.api_v1.services.base_schemas.schemas import GenericResponse
from api.api_v1.utils.work_with_money import WorkWithMoneyRepository
from core.models.base import Balance
from secure import JwtInfo
from typing import Callable
from sqlalchemy.ext.asyncio import AsyncSession

class UserBalanceService(UserBalanceServiceI):
    def __init__(self,
                 db_redis: Callable[..., Redis],
                 database_session:Callable[..., AsyncSession],
                 work_with_money: WorkWithMoneyRepository,
                 repository_balance:SQLAlchemyRepository,
                 settings_repository: SQLAlchemyRepository) -> None:
        self.session = database_session
        self.repository = repository_balance
        self.work_with_money = work_with_money
        self.repository_settings = settings_repository
        self.db_redis = db_redis

    async def get_balances(self, token: JwtInfo) -> GenericResponse[BalancesHistoryRead]:
        async with self.session() as session:
            result = await self.repository.find(session=session,validate=True,chat_id=token.id)
            settings = await self.repository_settings.find(session=session, validate=True, chat_id=token.id)
        convert_coef = 1
        if not "RUB" == settings.main_currency:
            async with self.db_redis() as session:
                price_base  = Decimal(await session.get("RUB"))
                price_convert = Decimal(await session.get(settings.main_currency))
                convert_coef = (price_base/price_convert).quantize(Decimal("0.00"), rounding=ROUND_HALF_UP)

        result = list(map(lambda x: (Decimal(x)/convert_coef).quantize(Decimal("0.00"), rounding=ROUND_HALF_UP),
                          result.balances_history.split()))
        result = BalancesHistoryRead(balances_history=result)
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
