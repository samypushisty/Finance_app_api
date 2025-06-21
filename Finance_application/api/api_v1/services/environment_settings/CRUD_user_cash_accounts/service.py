from sqlalchemy.orm import joinedload

from api.api_v1.utils.repository import SQLAlchemyRepository
from api.api_v1.utils.work_with_money import WorkWithMoneyRepository
from core.models.base import Balance, UserSettings, CashAccountCurrency, CashAccount
from .interface import UserCashAccountsServiceI
from api.api_v1.services.environment_settings.CRUD_user_cash_accounts.schemas import UserCashAccountPost, \
    UserCashAccountPatch, UserCashAccountsRead, UserCashAccountRead, UserCashAccountGet
from api.api_v1.services.base_schemas.schemas import GenericResponse, StandartException
from secure import JwtInfo
from typing import Callable
from sqlalchemy.ext.asyncio import AsyncSession
from  sqlalchemy import select

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
            result = await self.repository.find_all(session=session, validate=True, order_column="table_id", chat_id=token.id)
        result_accounts = UserCashAccountsRead(accounts=[])
        for i in result:
            data = UserCashAccountRead.model_validate(i, from_attributes=True)
            data.balance = await self.work_with_money.convert(base_currency=data.currency,
                                                              convert_currency="RUB",
                                                              amount=data.balance)
            result_accounts.accounts.append(data)
        return GenericResponse[UserCashAccountsRead](detail=result_accounts)


    async def get_user_cash_account(self,user_cash_account: UserCashAccountGet, token: JwtInfo) -> GenericResponse[UserCashAccountRead]:
        async with self.session() as session:
            result = await self.repository.find(session=session, validate=True,
                                                chat_id=token.id, table_id=user_cash_account.table_id)
        if user_cash_account.currency:
            result.currency = user_cash_account.currency
        result = UserCashAccountRead.model_validate(result, from_attributes=True)
        result.balance = await self.work_with_money.convert(base_currency=result.currency,
                                                       convert_currency="RUB",
                                                       amount=result.balance)
        return GenericResponse[UserCashAccountRead](detail=result)


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