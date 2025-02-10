from api.api_v1.services.CRUD_Movie_on_account.interface import UserMovieServiceI
from api.api_v1.services.CRUD_Movie_on_account.schemas import UserMoviePost, UserMoviePatch, UserMoviesRead, \
    UserMovieRead, UserMovieGet
from api.api_v1.utils.repository import SQLAlchemyRepository
from api.api_v1.services.base_schemas.schemas import GenericResponse, StandartException
from secure import JwtInfo
from typing import Callable
from sqlalchemy.ext.asyncio import AsyncSession

class UserMovieService(UserMovieServiceI):
    def __init__(self, repository: SQLAlchemyRepository, repository_cash_account: SQLAlchemyRepository, database_session:Callable[..., AsyncSession]) -> None:
        self.repository = repository
        self.repository_cash_account = repository_cash_account
        self.session = database_session

    async def post_movie(self, user_movie: UserMoviePost, token: JwtInfo) -> None:
        async with self.session() as session:
            async with session.begin():
                await self.repository.add(session=session,data={"chat_id": token.id,**user_movie.model_dump()})


    async def patch_movie(self, user_movie: UserMoviePatch, token: JwtInfo) -> None:
        async with self.session() as session:
            async with session.begin():
                await self.repository.patch(session=session, data=user_movie.model_dump(),chat_id=token.id,
                                    movie_id=user_movie.movie_id)


    async def get_movies(self, token: JwtInfo) -> GenericResponse[UserMoviesRead]:
        async with self.session() as session:
            async with session.begin():
                result = await self.repository.find_all(session=session, order_column="movie_id",chat_id=token.id)
        if not result:
            raise StandartException(status_code=404, detail="movie not found")
        result_movies = UserMoviesRead(movies=[])
        for i in result:
            result_movies.movies.append(UserMovieRead.model_validate(i, from_attributes=True))
        return GenericResponse[UserMoviesRead](detail=result_movies)


    async def get_movie(self, user_movie: UserMovieGet, token: JwtInfo) -> GenericResponse[UserMovieRead]:
        async with self.session() as session:
            result = await self.repository.find(session=session, chat_id=token.id,
                            movie_id=user_movie.movie_id)
        if not result:
            raise StandartException(status_code=404, detail="movie not found")
        result = UserMovieRead.model_validate(result, from_attributes=True)
        return GenericResponse[UserMovieRead](detail=result)

    async def delete_movie(self, user_movie: UserMovieGet, token: JwtInfo) -> None:
        async with self.session() as session:
            async with session.begin():
                await self.repository.delete(session=session,chat_id=token.id,movie_id=user_movie.movie_id)
