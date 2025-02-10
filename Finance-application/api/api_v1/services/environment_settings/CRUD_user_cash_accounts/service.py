from api.api_v1.utils.repository import SQLAlchemyRepository
from .interface import UserCashAccountsServiceI
from api.api_v1.services.environment_settings.CRUD_user_cash_accounts.schemas import UserCashAccountPost, \
    UserCashAccountPatch, UserCashAccountsRead, UserCashAccountRead, UserCashAccountGet
from api.api_v1.services.base_schemas.schemas import GenericResponse, StandartException
from secure import JwtInfo
from typing import Callable
from sqlalchemy.ext.asyncio import AsyncSession


class UserCashAccountsService(UserCashAccountsServiceI):
    def __init__(self, repository: SQLAlchemyRepository, database_session:Callable[..., AsyncSession]) -> None:
        self.repository = repository
        self.session = database_session


    async def post_user_category(self, user_cash_account: UserCashAccountPost,
        token: JwtInfo) -> None:
        async with self.session() as session:
            async with session.begin():
                await self.repository.add(session=session,data={"chat_id": token.id, **user_cash_account.model_dump()})


    async def patch_user_category(self, user_cash_account: UserCashAccountPatch, token: JwtInfo) -> None:
        async with self.session() as session:
            async with session.begin():
                await self.repository.patch(session=session,data=user_cash_account.model_dump(), chat_id=token.id,
                                            cash_id=user_cash_account.cash_id)


    async def get_user_categories(self, token: JwtInfo) -> GenericResponse[UserCashAccountsRead]:
        async with self.session() as session:
            result = await self.repository.find_all(session=session,order_column="cash_id", chat_id=token.id)
        if not result:
            raise StandartException(status_code=404, detail="cash account not found")
        result_accounts = UserCashAccountsRead(accounts=[])
        for i in result:
            result_accounts.accounts.append(UserCashAccountRead.model_validate(i, from_attributes=True))
        return GenericResponse[UserCashAccountsRead](detail=result_accounts)


    async def get_user_category(self,user_cash_account: UserCashAccountGet, token: JwtInfo) -> GenericResponse[UserCashAccountRead]:
        async with self.session() as session:
            result = await self.repository.find(session=session, chat_id=token.id,
                                            cash_id=user_cash_account.cash_id)
        if not result:
            raise StandartException(status_code=404, detail="cash account not found")
        result = UserCashAccountRead.model_validate(result, from_attributes=True)
        return GenericResponse[UserCashAccountRead](detail=result)


    async def delete_user_category(self,user_cash_account: UserCashAccountGet, token: JwtInfo) -> None:
        async with self.session() as session:
            async with session.begin():
                await self.repository.delete(session=session, chat_id=token.id, cash_id=user_cash_account.cash_id)
