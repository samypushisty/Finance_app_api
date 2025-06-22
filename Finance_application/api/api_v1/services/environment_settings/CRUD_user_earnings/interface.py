from abc import abstractmethod
from typing import Protocol

from secure import JwtInfo
from .schemas import UserTypeEarningsPost, UserTypeEarningsPatch, UserTypesEarningsRead, UserTypeEarningsGet, \
    UserTypeEarningsRead, UserTypeEarningsDelete
from api.api_v1.services.base_schemas.schemas import GenericResponse

class UserEarningsServiceI(Protocol):
    @abstractmethod
    async def post_user_type_of_earnings(self, user_type_of_earnings: UserTypeEarningsPost, token: JwtInfo) -> None:
        ...

    @abstractmethod
    async def patch_type_of_earnings(self, user_type_of_earnings: UserTypeEarningsPatch, token: JwtInfo) -> None:
        ...

    @abstractmethod
    async def get_types_of_earnings(self, token: JwtInfo) -> GenericResponse[UserTypesEarningsRead]:
        ...

    @abstractmethod
    async def get_type_of_earnings(self, user_type_of_earnings: UserTypeEarningsGet, token: JwtInfo) -> GenericResponse[UserTypeEarningsRead]:
        ...

    @abstractmethod
    async def delete_type_of_earnings(self, user_type_of_earnings: UserTypeEarningsDelete, token: JwtInfo) -> None:
        ...

