from abc import abstractmethod
from typing import Protocol

from secure import JwtInfo
from api.api_v1.services.environment_settings.CRUD_user_cash_accounts.schemas import UserCashAccountPost, \
    UserCashAccountPatch, UserCashAccountsRead, UserCashAccountRead, UserCashAccountGet
from api.api_v1.services.base_schemas.schemas import GenericResponse

class UserCashAccountsServiceI(Protocol):
    @abstractmethod
    async def post_user_cash_account(self, user_cash_account: UserCashAccountPost, token: JwtInfo) -> None:
        ...

    @abstractmethod
    async def patch_user_cash_account(self, user_cash_account: UserCashAccountPatch, token: JwtInfo) -> None:
        ...

    @abstractmethod
    async def get_user_cash_accounts(self, token: JwtInfo) -> GenericResponse[UserCashAccountsRead]:
        ...

    @abstractmethod
    async def get_user_cash_account(self,user_cash_account: UserCashAccountGet, token: JwtInfo) -> GenericResponse[UserCashAccountRead]:
        ...

    @abstractmethod
    async def delete_user_cash_account(self, user_cash_account: UserCashAccountGet, token: JwtInfo) -> None:
        ...

