from decimal import Decimal

from sqlalchemy.orm import joinedload, selectinload

from api.api_v1.utils.repository import SQLAlchemyRepository
from api.api_v1.utils.work_with_money import WorkWithMoneyRepository
from core.models.base import CashAccountCurrency, CashAccount
from .interface import UserCashAccountsServiceI
from api.api_v1.services.environment_settings.CRUD_user_cash_accounts.schemas import UserCashAccountPost, \
    UserCashAccountPatch, UserCashAccountsRead, UserCashAccountRead, UserCashAccountGet
from api.api_v1.services.base_schemas.schemas import GenericResponse, StandartException
from secure import JwtInfo
from typing import Callable
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, Result


class UserCashAccountsService(UserCashAccountsServiceI):
    def __init__(self, repository: SQLAlchemyRepository,
                 work_with_money:WorkWithMoneyRepository,
                 repository_balance: SQLAlchemyRepository,
                 repository_settings: SQLAlchemyRepository,
                 database_session:Callable[..., AsyncSession]) -> None:
        self.work_with_money = work_with_money
        self.repository = repository
        self.repository_balance = repository_balance
        self.repository_settings = repository_settings
        self.session = database_session


    async def post_user_cash_account(self, user_cash_account: UserCashAccountPost,
        token: JwtInfo) -> None:
        async with self.session() as session:
            async with session.begin():
                await self.repository.add(session=session,
                                          data={"chat_id": token.id,
                                                "currencies": [CashAccountCurrency(
                                                    chat_id=token.id,
                                                    currency=user_cash_account.currency,
                                                    amount=user_cash_account.balance
                                                ), ],
                                                "name":user_cash_account.name,
                                                "description":user_cash_account.description,
                                                "type":user_cash_account.type,
                                                "currency":user_cash_account.currency})


    async def patch_user_cash_account(self, user_cash_account: UserCashAccountPatch, token: JwtInfo) -> None:
        async with self.session() as session:
            async with session.begin():
                await self.repository.patch(session=session,data=user_cash_account.model_dump(exclude_unset=True),
                                            chat_id=token.id, table_id=user_cash_account.table_id)


    async def get_user_cash_accounts(self, token: JwtInfo) -> GenericResponse[UserCashAccountsRead]:
        async with self.session() as session:
            query = (
                select(CashAccount)
                .options(selectinload(CashAccount.currencies))
                .filter_by(chat_id=token.id)
                .order_by(CashAccount.table_id)
            )
            cash_accounts = await session.execute(query)
            cash_accounts = cash_accounts.scalars().all()
            if not cash_accounts:
                raise StandartException(status_code=404, detail="not found")
        result_accounts = UserCashAccountsRead(accounts=[])
        for cash_account in cash_accounts:
            balance = Decimal(0)
            for cash_currencies in cash_account.currencies:
                balance += await self.work_with_money.convert(base_currency=cash_account.currency,
                                                              convert_currency=cash_currencies.currency,
                                                              amount=cash_currencies.amount)
            response_data = UserCashAccountRead(
                table_id=cash_account.table_id,
                chat_id=cash_account.chat_id,
                name=cash_account.name,
                description=cash_account.description,
                type=cash_account.type,
                currency=cash_account.currency,
                balance=balance
            )
            result_accounts.accounts.append(response_data)
        return GenericResponse[UserCashAccountsRead](detail=result_accounts)


    async def get_user_cash_account(self,user_cash_account: UserCashAccountGet, token: JwtInfo) -> GenericResponse[UserCashAccountRead]:
        async with self.session() as session:
            query = (select(CashAccount).
                     options(joinedload(CashAccount.currencies)).
                     filter_by(chat_id=token.id, table_id=user_cash_account.table_id)
                     )
            cash_account: Result = await session.execute(query)
            cash_account: CashAccount = cash_account.scalars().first()
            if not cash_account:
                raise StandartException(status_code=404, detail="not found")
        target_currency = cash_account.currency
        if user_cash_account.currency:
            target_currency = user_cash_account.currency
        balance = Decimal(0)
        for cash_currencies in cash_account.currencies:
            balance += await self.work_with_money.convert(base_currency=target_currency,
                                                          convert_currency=cash_currencies.currency,
                                                          amount=cash_currencies.amount)
        response_data = UserCashAccountRead(
            table_id=cash_account.table_id,
            chat_id=cash_account.chat_id,
            name=cash_account.name,
            description=cash_account.description,
            type=cash_account.type,
            currency=target_currency,
            balance=balance
        )
        return GenericResponse[UserCashAccountRead](detail=response_data)


    async def delete_user_cash_account(self,user_cash_account: UserCashAccountGet, token: JwtInfo) -> None:
        async with self.session() as session:
            async with session.begin():
                cash_account = await self.repository.find(session=session, validate=True,
                                                          chat_id=token.id, table_id=user_cash_account.table_id)
                await self.repository.delete(session=session, chat_id=token.id, table_id=user_cash_account.table_id)
                await self.repository_balance.patch_field(session=session,
                                                          field="balance",
                                                          value=-cash_account.balance,
                                                          chat_id=token.id)