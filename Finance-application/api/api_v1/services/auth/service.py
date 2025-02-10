from api.api_v1.utils.repository import SQLAlchemyRepository
from api.api_v1.services.auth.schemas import UserAuth, UserRegistration, JWTRead
from api.api_v1.services.base_schemas.schemas import GenericResponse
from api.api_v1.services.user_settings.schemas import UserSettingsRead
from secure import create_jwt
from datetime import datetime, timezone
from typing import Callable
from sqlalchemy.ext.asyncio import AsyncSession

from api.api_v1.services.auth.interface import AuthServiceI

class AuthService(AuthServiceI):
    def __init__(self, repository_user: SQLAlchemyRepository, repository_settings: SQLAlchemyRepository, database_session:Callable[..., AsyncSession]) -> None:
        self.repository_user = repository_user
        self.repository_settings = repository_settings
        self.session = database_session


    async def get_user(self, user: UserAuth) -> GenericResponse[JWTRead]:
        async with self.session() as session:
            async with session.begin():
                result = await self.repository_user.find(session=session, chat_id=user.chat_id)
                if not result:
                    user_registration = UserRegistration(chat_id=user.chat_id)
                    user_settings = UserSettingsRead(chat_id=user.chat_id, theme="auto", language="english",
                                                            notifications=True, main_currency="usd")
                    await self.repository_user.add(session=session, data=user_registration.model_dump())
                    await self.repository_settings.add(session=session, data=user_settings.model_dump())
                else:
                    await self.repository_user.patch(session=session, data={"last_visit": datetime.now(timezone.utc).replace(tzinfo=None)}, chat_id=user.chat_id)
        answer = create_jwt(user.chat_id)
        return GenericResponse[JWTRead](detail=JWTRead(jwt=answer))
