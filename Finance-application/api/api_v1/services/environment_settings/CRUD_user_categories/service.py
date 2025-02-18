from api.api_v1.services.environment_settings.CRUD_user_categories.interface import UserCategoriesServiceI
from api.api_v1.services.environment_settings.CRUD_user_categories.schemas import UserCategoryPost, \
    UserCategoryPatch, UserCategoriesRead, UserCategoryRead, UserCategoryGet
from api.api_v1.utils.repository import SQLAlchemyRepository
from api.api_v1.services.base_schemas.schemas import GenericResponse, StandartException
from secure import JwtInfo
from typing import Callable
from sqlalchemy.ext.asyncio import AsyncSession


class UserCategoriesService(UserCategoriesServiceI):
    def __init__(self,repository:SQLAlchemyRepository, database_session:Callable[..., AsyncSession]) -> None:
        self.repository = repository
        self.session = database_session

    async def post_user_category(self, user_category: UserCategoryPost,
        token: JwtInfo) -> None:
        async with self.session() as session:
            async with session.begin():
                await self.repository.add(session=session,data={"chat_id": token.id,**user_category.model_dump()})


    async def patch_user_category(self, user_category: UserCategoryPatch, token: JwtInfo) -> None:
        async with self.session() as session:
            async with session.begin():
                await self.repository.patch(session=session, data=user_category.model_dump(exclude_unset=True),
                                            chat_id=token.id, category_id=user_category.category_id)


    async def get_user_categories(self, token: JwtInfo) -> GenericResponse[UserCategoriesRead]:
        async with self.session() as session:
            result = await self.repository.find_all(session=session,order_column="category_id",chat_id=token.id)
        if not result:
            raise StandartException(status_code=404, detail="categories not found")
        result_categories = UserCategoriesRead(categories=[])
        for i in result:
            result_categories.categories.append(UserCategoryRead.model_validate(i, from_attributes=True))
        return GenericResponse[UserCategoriesRead](detail=result_categories)


    async def get_user_category(self,user_category: UserCategoryGet, token: JwtInfo) -> GenericResponse[UserCategoryRead]:
        async with self.session() as session:
            result = await self.repository.find(session=session, chat_id=token.id,
                            category_id=user_category.category_id)
        if not result:
            raise StandartException(status_code=404, detail="category not found")
        result = UserCategoryRead.model_validate(result, from_attributes=True)
        return GenericResponse[UserCategoryRead](detail=result)


    async def delete_user_category(self,user_category: UserCategoryGet, token: JwtInfo) -> None:
        async with self.session() as session:
            async with session.begin():
                await self.repository.delete(session=session, chat_id=token.id,category_id=user_category.category_id)
