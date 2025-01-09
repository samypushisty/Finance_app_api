from api.api_v1.utils.repository import SQLAlchemyRepository
from .interface import UserCashAccountsServiceI
from api.api_v1.services.environment_settings.CRUD_user_cash_accounts.schemas import UserCashAccountPost, \
    UserCashAccountPatch, UserCashAccountsRead, UserCashAccountRead, UserCashAccountGet
from api.api_v1.services.base_schemas.schemas import GenericResponse, StandartException
from secure import JwtInfo

class UserCashAccountsService(UserCashAccountsServiceI):
    def __init__(self, repository: SQLAlchemyRepository) -> None:
        self.repository = repository


    async def post_user_category(self, user_cash_account: UserCashAccountPost,
        token: JwtInfo) -> None:
        await self.repository.add({"chat_id": token.id, **user_cash_account.model_dump()})


    async def patch_user_category(self, user_cash_account: UserCashAccountPatch, token: JwtInfo) -> None:
        await self.repository.patch(user_cash_account.model_dump(), chat_id=token.id,
                                    cash_id=user_cash_account.cash_id)


    async def get_user_categories(self, token: JwtInfo) -> GenericResponse[UserCashAccountsRead]:
        result = await self.repository.find_all(order_column="cash_id", chat_id=token.id)
        if not result:
            raise StandartException(status_code=404, detail="cash account not found")
        result_accounts = UserCashAccountsRead(accounts=[])
        for i in result:
            result_accounts.accounts.append(UserCashAccountRead.model_validate(i, from_attributes=True))
        return GenericResponse[UserCashAccountsRead](detail=result_accounts)


    async def get_user_category(self,user_cash_account: UserCashAccountGet, token: JwtInfo) -> GenericResponse[UserCashAccountRead]:
        result = await self.repository.find(chat_id=token.id,
                                            cash_id=user_cash_account.cash_id)
        if not result:
            raise StandartException(status_code=404, detail="cash account not found")
        result = UserCashAccountRead.model_validate(result, from_attributes=True)
        return GenericResponse[UserCashAccountRead](detail=result)


    async def delete_user_category(self,user_cash_account: UserCashAccountGet, token: JwtInfo) -> None:
        await self.repository.delete(chat_id=token.id, cash_id=user_cash_account.cash_id)
