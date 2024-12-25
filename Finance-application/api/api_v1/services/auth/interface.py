from abc import abstractmethod
from typing import Protocol

from .schemas import UserAuth, JWTRead
from api.api_v1.services.base_schemas.schemas import GenericResponse

class AuthServiceI(Protocol):
    @abstractmethod
    async def get_user(self, user: UserAuth) -> GenericResponse[JWTRead]:
        ...
