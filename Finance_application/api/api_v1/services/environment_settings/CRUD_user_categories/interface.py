from abc import abstractmethod
from typing import Protocol

from secure import JwtInfo
from .schemas import UserCategoryGet, UserCategoryPost, UserCategoryPatch, UserCategoriesRead, UserCategoryRead, \
    UserCategoryDelete
from api.api_v1.services.base_schemas.schemas import GenericResponse

class UserCategoriesServiceI(Protocol):
    @abstractmethod
    async def post_user_category(self, user_category: UserCategoryPost, token: JwtInfo) -> None:
        ...

    @abstractmethod
    async def patch_user_category(self, user_category: UserCategoryPatch, token: JwtInfo) -> None:
        ...

    @abstractmethod
    async def get_user_categories(self, token: JwtInfo) -> GenericResponse[UserCategoriesRead]:
        ...

    @abstractmethod
    async def get_user_category(self,user_category: UserCategoryGet, token: JwtInfo) -> GenericResponse[UserCategoryRead]:
        ...

    @abstractmethod
    async def delete_user_category(self, user_category: UserCategoryDelete, token: JwtInfo) -> None:
        ...

