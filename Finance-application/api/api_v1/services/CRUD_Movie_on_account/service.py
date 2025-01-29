from api.api_v1.services.CRUD_Movie_on_account.interface import UserMovieServiceI
from api.api_v1.services.CRUD_Movie_on_account.schemas import UserMoviePost, UserMoviePatch, UserMoviesRead, \
    UserMovieRead, UserMovieGet
from api.api_v1.utils.repository import SQLAlchemyRepository
from api.api_v1.services.base_schemas.schemas import GenericResponse, StandartException
from secure import JwtInfo


class UserMovieService(UserMovieServiceI):
    def __init__(self,repository:SQLAlchemyRepository) -> None:
        self.repository = repository

    async def post_movie(self, user_movie: UserMoviePost, token: JwtInfo) -> None:
        await self.repository.add({"chat_id": token.id,**user_movie.model_dump()})


    async def patch_movie(self, user_movie: UserMoviePatch, token: JwtInfo) -> None:
        await self.repository.patch(user_movie.model_dump(),chat_id=token.id,
                               movie_id=user_movie.movie_id)


    async def get_movies(self, token: JwtInfo) -> GenericResponse[UserMoviesRead]:
        result = await self.repository.find_all(order_column="movie_id",chat_id=token.id)
        if not result:
            raise StandartException(status_code=404, detail="movie not found")
        result_movies = UserMoviesRead(movies=[])
        for i in result:
            result_movies.movies.append(UserMovieRead.model_validate(i, from_attributes=True))
        return GenericResponse[UserMoviesRead](detail=result_movies)


    async def get_movie(self, user_movie: UserMovieGet, token: JwtInfo) -> GenericResponse[UserMovieRead]:
        result = await self.repository.find(chat_id=token.id,
                           movie_id=user_movie.movie_id)
        if not result:
            raise StandartException(status_code=404, detail="movie not found")
        result = UserMovieRead.model_validate(result, from_attributes=True)
        return GenericResponse[UserMovieRead](detail=result)

    async def delete_movie(self, user_movie: UserMovieGet, token: JwtInfo) -> None:
        await self.repository.delete(chat_id=token.id,movie_id=user_movie.movie_id)
