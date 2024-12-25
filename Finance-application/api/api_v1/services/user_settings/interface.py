from abc import abstractmethod
from typing import Protocol

from secure import JwtInfo
from .schemas import UserSettingsRead, UserSettingsPatch
from api.api_v1.services.base_schemas.schemas import GenericResponse

class UserSettingsServiceI(Protocol):
    @abstractmethod
    async def patch_settings(self, user_settings: UserSettingsPatch, token: JwtInfo) -> None:
        ...

    async def get_settings(self, token: JwtInfo) -> GenericResponse[UserSettingsRead]:
        ...