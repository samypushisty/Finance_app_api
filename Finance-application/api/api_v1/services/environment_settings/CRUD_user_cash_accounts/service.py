from typing import Callable

from httpx import delete
from sqlalchemy.ext.asyncio import AsyncSession

from .interface import UserCashAccountsServiceI
from api.api_v1.services.environment_settings.CRUD_user_cash_accounts.schemas import UserCashAccountPost, \
    UserCashAccountPatch, UserCashAccountsRead, UserCashAccountRead, UserCashAccountGet
from api.api_v1.services.base_schemas.schemas import GenericResponse, StandartException
from secure import JwtInfo
from sqlalchemy import select, update, delete
from core.models.base import CashAccount

class UserCashAccountsService(UserCashAccountsServiceI):
    def __init__(self, session: Callable[..., AsyncSession]) -> None:
        self.session = session

    async def post_user_category(self, user_cash_account: UserCashAccountPost,
        token: JwtInfo) -> None:
        async with self.session() as session:
            async with session.begin():
                stmt = CashAccount(chat_id=token.id,**user_cash_account.model_dump())
                session.add(stmt)
                await session.commit()


    async def patch_user_category(self, user_cash_account: UserCashAccountPatch, token: JwtInfo) -> None:
        async with self.session() as session:
            async with session.begin():
                stmt = (
                    update(CashAccount)
                    .values(**user_cash_account.model_dump())
                    .filter(CashAccount.chat_id == token.id)
                    .filter(CashAccount.cash_id == user_cash_account.cash_id)
                )
                result = await session.execute(stmt)
                if result.rowcount == 0:
                    await session.rollback()
                    raise StandartException(status_code=404, detail="user or cash account not found")
                await session.commit()


    async def get_user_categories(self, token: JwtInfo) -> GenericResponse[UserCashAccountsRead]:

        async with self.session() as session:
            query = (
                select(CashAccount)
                .filter(CashAccount.chat_id == token.id)
                .order_by(CashAccount.cash_id)
            )
            result = await session.execute(query)
            result = result.scalars().all()
            if not result:
                raise StandartException(status_code=404, detail="cash accounts not found")
            result_accounts = UserCashAccountsRead(accounts=[])
            for i in result:
                result_accounts.accounts.append(UserCashAccountRead.model_validate(i, from_attributes=True))
            return GenericResponse[UserCashAccountsRead](detail=result_accounts)


    async def get_user_category(self,user_cash_account: UserCashAccountGet, token: JwtInfo) -> GenericResponse[UserCashAccountRead]:

        async with self.session() as session:
            query = (
                select(CashAccount)
                .filter(CashAccount.chat_id == token.id)
                .filter(CashAccount.cash_id == user_cash_account.cash_id)
            )
            result = await session.execute(query)
            result = result.scalars().first()
            if not result:
                raise StandartException(status_code=404, detail="account not found")
            result = UserCashAccountRead.model_validate(result, from_attributes=True)
            return GenericResponse[UserCashAccountRead](detail=result)

    async def delete_user_category(self,user_cash_account: UserCashAccountGet, token: JwtInfo) -> None:
        async with self.session() as session:
            query = (
                delete(CashAccount)
                .filter(CashAccount.chat_id == token.id)
                .filter(CashAccount.cash_id == user_cash_account.cash_id)
            )
            result = await session.execute(query)
            if result.rowcount == 0:
                await session.rollback()
                raise StandartException(status_code=404, detail="cash account not found")
            await session.commit()