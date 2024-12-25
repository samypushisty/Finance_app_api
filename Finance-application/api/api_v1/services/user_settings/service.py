from typing import Callable
from sqlalchemy.ext.asyncio import AsyncSession
from api.api_v1.services.user_settings.interface import UserSettingsServiceI
from core.models.base import Settings
from api.api_v1.services.base_schemas.schemas import GenericResponse
from api.api_v1.services.user_settings.schemas import UserSettingsRead, UserSettingsPatch
from secure import JwtInfo
from sqlalchemy import select


class UserSettingsService(UserSettingsServiceI):
    def __init__(self, session: Callable[..., AsyncSession]) -> None:
        self.session = session

    async def patch_settings(self, user_settings: UserSettingsPatch,
        token: JwtInfo) -> None:
        async with self.session() as session:
            async with session.begin():
                query = select(Settings).filter(Settings.chat_id == token.id)
                user_settings_old = await session.execute(query)
                user_settings_old = user_settings_old.scalars().first()
                for key in user_settings.model_dump().keys():
                    if not getattr(user_settings, key) == getattr(user_settings_old, key):
                        setattr(user_settings_old, key, getattr(user_settings, key))
                await session.commit()

    async def get_settings(self, token: JwtInfo) -> GenericResponse[UserSettingsRead]:
        async with self.session() as session:
            query = select(Settings).where(Settings.chat_id == token.id)
            result = await session.execute(query)
            result = UserSettingsRead.model_validate(result.scalars().first(),from_attributes=True)
            return GenericResponse[UserSettingsRead](detail=result)