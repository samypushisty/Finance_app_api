from api.api_v1.services.user_settings.interface import UserSettingsServiceI
from api.api_v1.utils.repository import SQLAlchemyRepository
from api.api_v1.services.base_schemas.schemas import GenericResponse, StandartException
from api.api_v1.services.user_settings.schemas import UserSettingsRead, UserSettingsPatch
from secure import JwtInfo
from typing import Callable
from sqlalchemy.ext.asyncio import AsyncSession


class UserSettingsService(UserSettingsServiceI):
    def __init__(self,repository: SQLAlchemyRepository, database_session:Callable[..., AsyncSession]) -> None:
        self.repository = repository
        self.session = database_session

    async def patch_settings(self, user_settings: UserSettingsPatch,
        token: JwtInfo) -> None:
        async with self.session() as session:
            async with session.begin():
                await self.repository.patch(session=session, data=user_settings.model_dump(), chat_id=token.id)


    async def get_settings(self, token: JwtInfo) -> GenericResponse[UserSettingsRead]:
        async with self.session() as session:
            result = await self.repository.find(session=session, chat_id=token.id)
        if not result:
            raise StandartException(status_code=404, detail="user not found")
        result = UserSettingsRead.model_validate(result,from_attributes=True)
        return GenericResponse[UserSettingsRead](detail=result)