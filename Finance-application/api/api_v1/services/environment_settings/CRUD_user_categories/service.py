from api.api_v1.services.environment_settings.CRUD_user_categories.interface import UserCategoriesServiceI
from api.api_v1.services.environment_settings.CRUD_user_categories.schemas import UserCategoryPost, \
    UserCategoryPatch, UserCategoriesRead, UserCategoryRead, UserCategoryGet
from api.api_v1.utils.repository import SQLAlchemyRepository
from api.api_v1.services.base_schemas.schemas import GenericResponse, StandartException
from secure import JwtInfo


class UserCategoriesService(UserCategoriesServiceI):
    def __init__(self,repository:SQLAlchemyRepository) -> None:
        self.repository = repository

    async def post_user_category(self, user_category: UserCategoryPost,
        token: JwtInfo) -> None:
        await self.repository.add({"chat_id": token.id,**user_category.model_dump()})


    async def patch_user_category(self, user_category: UserCategoryPatch, token: JwtInfo) -> None:
        await self.repository.patch(user_category.model_dump(),chat_id=token.id,
                               category_id=user_category.category_id)


    async def get_user_categories(self, token: JwtInfo) -> GenericResponse[UserCategoriesRead]:
        result = await self.repository.find_all(order_column="category_id",chat_id=token.id)
        if not result:
            raise StandartException(status_code=404, detail="categories not found")
        result_categories = UserCategoriesRead(categories=[])
        for i in result:
            result_categories.categories.append(UserCategoryRead.model_validate(i, from_attributes=True))
        return GenericResponse[UserCategoriesRead](detail=result_categories)


    async def get_user_category(self,user_category: UserCategoryGet, token: JwtInfo) -> GenericResponse[UserCategoryRead]:
        result = await self.repository.find(chat_id=token.id,
                           category_id=user_category.category_id)
        if not result:
            raise StandartException(status_code=404, detail="category not found")
        result = UserCategoryRead.model_validate(result, from_attributes=True)
        return GenericResponse[UserCategoryRead](detail=result)


    async def delete_user_category(self,user_category: UserCategoryGet, token: JwtInfo) -> None:
        await self.repository.delete(chat_id=token.id,category_id=user_category.category_id)
