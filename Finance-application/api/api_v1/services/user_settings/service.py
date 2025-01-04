from typing import Callable
from sqlalchemy.ext.asyncio import AsyncSession
from api.api_v1.services.user_settings.interface import UserSettingsServiceI
from core.models.base import Settings
from api.api_v1.services.base_schemas.schemas import GenericResponse, StandartException
from api.api_v1.services.user_settings.schemas import UserSettingsRead, UserSettingsPatch
from secure import JwtInfo
from sqlalchemy import select, update


class UserSettingsService(UserSettingsServiceI):
    def __init__(self, session: Callable[..., AsyncSession]) -> None:
        self.session = session

    async def patch_settings(self, user_settings: UserSettingsPatch,
        token: JwtInfo) -> None:
        async with self.session() as session:
            async with session.begin():
                stmt = (
                    update(Settings)
                    .values(**user_settings.model_dump())
                    .filter(Settings.chat_id == token.id)
                )
                result = await session.execute(stmt)
                if result.rowcount == 0:
                    await session.rollback()
                    raise StandartException(status_code=404, detail="user not found")
                await session.commit()


    async def get_settings(self, token: JwtInfo) -> GenericResponse[UserSettingsRead]:
        async with self.session() as session:
            query = (
                select(Settings)
                .where(Settings.chat_id == token.id)
            )
            result = await session.execute(query)
            result = result.scalars().first()
            if not result:
                raise StandartException(status_code=404,detail="user not found")
            result = UserSettingsRead.model_validate(result,from_attributes=True)
            return GenericResponse[UserSettingsRead](detail=result)