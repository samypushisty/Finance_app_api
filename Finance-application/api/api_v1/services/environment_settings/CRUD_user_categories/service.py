from typing import Callable
from sqlalchemy.ext.asyncio import AsyncSession

from api.api_v1.services.environment_settings.CRUD_user_categories.interface import UserCategoriesServiceI
from api.api_v1.services.environment_settings.CRUD_user_categories.schemas import UserCategoryPost, \
    UserCategoryPatch, UserCategoriesRead, UserCategoryRead, UserCategoryGet
from core.models.base import Category
from api.api_v1.services.base_schemas.schemas import GenericResponse, StandartException
from secure import JwtInfo
from sqlalchemy import select


class UserCategoriesService(UserCategoriesServiceI):
    def __init__(self, session: Callable[..., AsyncSession]) -> None:
        self.session = session

    async def post_user_category(self, user_category: UserCategoryPost,
        token: JwtInfo) -> None:
        async with self.session() as session:
            async with session.begin():
                stmt = Category(chat_id=token.id,**user_category.model_dump())
                session.add(stmt)
                await session.commit()


    async def patch_user_category(self, user_category: UserCategoryPatch, token: JwtInfo) -> None:
        async with self.session() as session:
            async with session.begin():
                query = select(Category).filter(Category.chat_id == token.id).filter(
                    Category.category_id == user_category.category_id)
                category_id_old = await session.execute(query)
                category_id_old = category_id_old.scalars().first()
                if not category_id_old:
                    raise StandartException(status_code=404, detail="category not found")
                for key in user_category.model_dump().keys():
                    if not getattr(user_category, key) == getattr(category_id_old, key):
                        setattr(category_id_old, key, getattr(user_category, key))
                await session.commit()


    async def get_user_categories(self, token: JwtInfo) -> GenericResponse[UserCategoriesRead]:

        async with self.session() as session:
            query = select(Category).filter(Category.chat_id == token.id).order_by(Category.category_id)
            result = await session.execute(query)
            result = result.scalars().all()
            if not result:
                raise StandartException(status_code=404, detail="categories not found")
            result_categories = UserCategoriesRead(categories=[])
            for i in result:
                result_categories.categories.append(UserCategoryRead.model_validate(i, from_attributes=True))
            return GenericResponse[UserCategoriesRead](detail=result_categories)


    async def get_user_category(self,user_category: UserCategoryGet, token: JwtInfo) -> GenericResponse[UserCategoryRead]:

        async with self.session() as session:
            query = select(Category).filter(Category.chat_id == token.id).filter(
                Category.category_id == user_category.category_id)
            result = await session.execute(query)
            result = result.scalars().first()
            if not result:
                raise StandartException(status_code=404, detail="category not found")
            result = UserCategoryRead.model_validate(result, from_attributes=True)
            return GenericResponse[UserCategoryRead](detail=result)

    async def delete_user_category(self,user_category: UserCategoryGet, token: JwtInfo) -> None:
        async with self.session() as session:
            query = select(Category).filter(Category.chat_id == token.id).filter(
                Category.category_id == user_category.category_id)
            result = await session.execute(query)
            result = result.scalars().first()
            if not result:
                raise StandartException(status_code=404,detail="category not found")
            await session.delete(result)
            await session.commit()