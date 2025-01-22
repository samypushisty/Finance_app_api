from api.api_v1.services.environment_settings.CRUD_user_earnings.interface import UserEarningsServiceI
from api.api_v1.services.environment_settings.CRUD_user_earnings.schemas import UserTypeEarningsPost, \
    UserTypeEarningsPatch, UserTypesEarningsRead, UserTypeEarningsRead, UserTypeEarningsGet
from api.api_v1.utils.repository import SQLAlchemyRepository
from api.api_v1.services.base_schemas.schemas import GenericResponse, StandartException
from secure import JwtInfo


class UserEarningsService(UserEarningsServiceI):
    def __init__(self,repository:SQLAlchemyRepository) -> None:
        self.repository = repository

    async def post_user_type_of_earnings(self, user_type_of_earnings: UserTypeEarningsPost, token: JwtInfo) -> None:
        await self.repository.add({"chat_id": token.id,**user_type_of_earnings.model_dump()})


    async def patch_type_of_earnings(self, user_type_of_earnings: UserTypeEarningsPatch, token: JwtInfo) -> None:
        await self.repository.patch(user_type_of_earnings.model_dump(),chat_id=token.id,
                               earning_id=user_type_of_earnings.earning_id)


    async def get_types_of_earnings(self, token: JwtInfo) -> GenericResponse[UserTypesEarningsRead]:
        result = await self.repository.find_all(order_column="earning_id",chat_id=token.id)
        if not result:
            raise StandartException(status_code=404, detail="types of earnings not found")
        result_types = UserTypesEarningsRead(types_of_earnings=[])
        for i in result:
            result_types.types_of_earnings.append(UserTypeEarningsRead.model_validate(i, from_attributes=True))
        return GenericResponse[UserTypesEarningsRead](detail=result_types)


    async def get_type_of_earnings(self, user_type_of_earnings: UserTypeEarningsGet, token: JwtInfo) -> GenericResponse[UserTypeEarningsRead]:
        result = await self.repository.find(chat_id=token.id,
                           earning_id=user_type_of_earnings.earning_id)
        if not result:
            raise StandartException(status_code=404, detail="type of earnings not found")
        result = UserTypeEarningsRead.model_validate(result, from_attributes=True)
        return GenericResponse[UserTypeEarningsRead](detail=result)

    async def delete_type_of_earnings(self, user_type_of_earnings: UserTypeEarningsGet, token: JwtInfo) -> None:
        await self.repository.delete(chat_id=token.id,earning_id=user_type_of_earnings.earning_id)
