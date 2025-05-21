from abc import abstractmethod
from typing import Protocol

from api.api_v1.services.CRUD_Movie_on_account.schemas import UserMoviePost, UserMoviePatch, UserMoviesRead, \
    UserMovieGet, UserMovieRead, UserMoviesGet
from secure import JwtInfo
from api.api_v1.services.base_schemas.schemas import GenericResponse

class UserMovieServiceI(Protocol):
    @abstractmethod
    async def post_movie(self, user_movie: UserMoviePost, token: JwtInfo) -> None:
        ...

    @abstractmethod
    async def patch_movie(self, user_movie: UserMoviePatch, token: JwtInfo) -> None:
        ...

    @abstractmethod
    async def get_movies(self, user_movie: UserMoviesGet, token: JwtInfo) -> GenericResponse[UserMoviesRead]:
        ...

    @abstractmethod
    async def get_movie(self, user_movie: UserMovieGet, token: JwtInfo) -> GenericResponse[UserMovieRead]:
        ...

    @abstractmethod
    async def delete_movie(self, user_movie: UserMovieGet, token: JwtInfo) -> None:
        ...

