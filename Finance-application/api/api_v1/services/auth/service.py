from api.api_v1.utils.repository import SQLAlchemyRepository
from api.api_v1.services.auth.schemas import UserAuth, UserRegistration, JWTRead
from api.api_v1.services.base_schemas.schemas import GenericResponse
from api.api_v1.services.user_settings.schemas import UserSettingsRead
from secure import create_jwt


from api.api_v1.services.auth.interface import AuthServiceI

class AuthService(AuthServiceI):
    def __init__(self, repository_user: SQLAlchemyRepository, repository_settings: SQLAlchemyRepository) -> None:
        self.repository_user = repository_user
        self.repository_settings = repository_settings

    async def get_user(self, user: UserAuth) -> GenericResponse[JWTRead]:
        result = await self.repository_user.find(chat_id=user.chat_id)
        if not result:
            user_registration = UserRegistration(chat_id=user.chat_id, currencies="_", type_of_earnings="_")
            user_settings = UserSettingsRead(chat_id=user.chat_id, theme="auto", language="english",
                                                     notifications=True, main_currency="usd")
            await self.repository_user.add(user_registration.model_dump())
            await self.repository_settings.add(user_settings.model_dump())
        answer = create_jwt(user.chat_id)
        return GenericResponse[JWTRead](detail=JWTRead(jwt=answer))
