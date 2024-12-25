from typing import Callable
from sqlalchemy.ext.asyncio import AsyncSession
from core.models.base import User, Settings
from api.api_v1.services.auth.schemas import UserAuth, UserRegistration, JWTRead
from api.api_v1.services.base_schemas.schemas import GenericResponse
from api.api_v1.services.user_settings.schemas import UserSettingsRead
from secure import create_jwt
from sqlalchemy import select


from api.api_v1.services.auth.interface import AuthServiceI

class AuthService(AuthServiceI):
    def __init__(self, session: Callable[..., AsyncSession]) -> None:
        self.session = session

    async def get_user(self, user: UserAuth) -> GenericResponse[JWTRead]:
        async with self.session() as session:
            async with session.begin():
                query = select(User).where(User.chat_id == user.chat_id)
                result = await session.execute(query)
                result = result.scalars().all()
                if not result:
                    user_registration = UserRegistration(chat_id=user.chat_id, currencies="_", type_of_earnings="_")
                    user_settings = UserSettingsRead(chat_id=user.chat_id, theme="auto", language="english",
                                                     notifications=True, main_currency="usd")
                    stmt = User(**user_registration.model_dump())
                    session.add(stmt)
                    await session.flush()
                    stmt = Settings(**user_settings.model_dump())
                    session.add(stmt)
                    await session.commit()
                answer = create_jwt(user.chat_id)
                return GenericResponse[JWTRead](detail=JWTRead(jwt=answer))
