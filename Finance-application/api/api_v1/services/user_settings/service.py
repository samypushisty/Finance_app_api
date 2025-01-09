from api.api_v1.services.user_settings.interface import UserSettingsServiceI
from api.api_v1.utils.repository import SQLAlchemyRepository
from api.api_v1.services.base_schemas.schemas import GenericResponse, StandartException
from api.api_v1.services.user_settings.schemas import UserSettingsRead, UserSettingsPatch
from secure import JwtInfo


class UserSettingsService(UserSettingsServiceI):
    def __init__(self,repository: SQLAlchemyRepository) -> None:
        self.repository = repository

    async def patch_settings(self, user_settings: UserSettingsPatch,
        token: JwtInfo) -> None:
        await self.repository.patch(user_settings.model_dump(), chat_id=token.id)


    async def get_settings(self, token: JwtInfo) -> GenericResponse[UserSettingsRead]:
        result = await self.repository.find(chat_id=token.id)
        if not result:
            raise StandartException(status_code=404, detail="user not found")
        result = UserSettingsRead.model_validate(result,from_attributes=True)
        return GenericResponse[UserSettingsRead](detail=result)