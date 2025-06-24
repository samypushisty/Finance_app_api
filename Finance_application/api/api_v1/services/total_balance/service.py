from decimal import Decimal, ROUND_HALF_UP

from redis import Redis
from sqlalchemy import select, Result
from sqlalchemy.orm import selectinload

from api.api_v1.services.total_balance.interface import UserBalanceServiceI
from api.api_v1.services.total_balance.schemas import BalanceRead, BalancesHistoryRead, BalanceGet
from api.api_v1.utils.repository import SQLAlchemyRepository
from api.api_v1.services.base_schemas.schemas import GenericResponse, StandartException
from api.api_v1.utils.work_with_money import WorkWithMoneyRepository
from core.models.base import CashAccount
from secure import JwtInfo
from typing import Callable, Sequence
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

    async def get_balances(self, balance: BalanceGet, token: JwtInfo) -> GenericResponse[BalancesHistoryRead]:
        async with self.session() as session:
            result = await self.repository.find(session=session,validate=True,chat_id=token.id)
            if balance.currency:
                currency = balance.currency
            else:
                settings = await self.repository_settings.find(session=session, validate=True, chat_id=token.id)
                currency = settings.main_currency

        convert_coef = 1

        if not "RUB" == currency:
            async with self.db_redis() as session:
                price_base  = Decimal(await session.get("RUB"))
                price_convert = Decimal(await session.get(currency))
                convert_coef = (price_base/price_convert).quantize(Decimal("0.00"), rounding=ROUND_HALF_UP)

        result = list(map(lambda x: (Decimal(x)/convert_coef).quantize(Decimal("0.00"), rounding=ROUND_HALF_UP),
                          result.balances_history.split()))
        result = BalancesHistoryRead(balances_history=result)
        return GenericResponse[BalancesHistoryRead](detail=result)


    async def get_balance(self, balance: BalanceGet, token: JwtInfo) -> GenericResponse[BalanceRead]:
        async with self.session() as session:
            query = (select(CashAccount).
                     options(selectinload(CashAccount.currencies_earnings), selectinload(CashAccount.currencies_outlays)).
                     filter_by(chat_id=token.id)
                     )
            cash_accounts: Result = await session.execute(query)
            cash_accounts: Sequence[CashAccount] = cash_accounts.scalars().all()

            if not cash_accounts:
                raise StandartException(status_code=404, detail="not found")

            if balance.currency:
                target_currency = balance.currency
            else:
                settings = await self.repository_settings.find(session=session, validate=True, chat_id=token.id)
                target_currency = settings.main_currency

            amount_currencies = {}
            for cash_account in cash_accounts:
                for currencies_earnings in cash_account.currencies_earnings:
                    if not currencies_earnings.currency in amount_currencies:
                        amount_currencies[currencies_earnings.currency] = currencies_earnings.amount
                    else:
                        amount_currencies[currencies_earnings.currency] += currencies_earnings.amount
            for cash_account in cash_accounts:
                for currencies_outlays in cash_account.currencies_outlays:
                    amount_currencies[currencies_outlays.currency] -= currencies_outlays.amount

            balance = Decimal('0.00').quantize(Decimal('0.00'))
            for currency, amount in amount_currencies.items():
                balance += await self.work_with_money.convert(base_currency=target_currency,
                                                              convert_currency=currency,
                                                              amount=amount)

            response_data = BalanceRead(
                chat_id=cash_account.chat_id,
                balance=balance
            )
            return GenericResponse[BalanceRead](detail=response_data)
