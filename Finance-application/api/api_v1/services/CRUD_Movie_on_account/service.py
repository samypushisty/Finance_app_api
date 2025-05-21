from api.api_v1.services.CRUD_Movie_on_account.interface import UserMovieServiceI
from api.api_v1.services.CRUD_Movie_on_account.schemas import UserMoviePost, UserMoviePatch, UserMoviesRead, \
    UserMovieRead, UserMovieGet, UserMoviesGet
from api.api_v1.utils.work_with_money import WorkWithMoneyRepository
from api.api_v1.utils.repository import SQLAlchemyRepository
from api.api_v1.services.base_schemas.schemas import GenericResponse
from core.models.base import MovieOnAccount
from secure import JwtInfo
from typing import Callable
from sqlalchemy.ext.asyncio import AsyncSession

class UserMovieService(UserMovieServiceI):
    def __init__(self,
                 work_with_money:WorkWithMoneyRepository,
                 repository: SQLAlchemyRepository,
                 database_session:Callable[..., AsyncSession]) -> None:
        self.work_with_money = work_with_money
        self.repository = repository
        self.session = database_session


    async def post_movie(self, user_movie: UserMoviePost, token: JwtInfo) -> None:
        worth = await self.work_with_money.convert(base_currency="RUB",
                                                   convert_currency=user_movie.currency,
                                                   amount=user_movie.worth)
        async with self.session() as session:
            async with session.begin():

                # добавление операции
                await self.repository.add(session=session, data={"chat_id": token.id, "base_worth": worth,
                                                                 **user_movie.model_dump()})
                # изменение балансов
                await self.work_with_money.add_transaction(session=session,
                                                           chat_id=token.id,
                                                           cash_id=user_movie.cash_account,
                                                           category_id=user_movie.categories_id,
                                                           earning_id=user_movie.earnings_id,
                                                           type_operation=user_movie.type,
                                                           amount=worth)



    async def patch_movie(self, user_movie: UserMoviePatch, token: JwtInfo) -> None:
        async with self.session() as session:
            async with session.begin():
                patch_data = user_movie.model_dump(exclude_unset=True)
                if user_movie.worth or user_movie.currency:
                    # получение информации
                    old_movie: MovieOnAccount = await self.repository.find(session=session, validate=True,
                                                                           chat_id=token.id, table_id=user_movie.table_id)

                    # полуение валют
                    if not user_movie.currency:
                        movie_currency = old_movie.currency
                    else:
                        movie_currency = user_movie.currency

                    # получение старой стоймостей
                    if not user_movie.worth:
                        movie_worth = old_movie.worth
                    else:
                        movie_worth = user_movie.worth

                    # получение конвертированной стоймости общего аккаунта
                    new_worth = await self.work_with_money.convert(base_currency="RUB",
                                                                       convert_currency=movie_currency,
                                                                       amount=movie_worth)
                    # изменение баланса
                    await self.work_with_money.edit_transaction(session=session,
                                                                chat_id=token.id,
                                                                cash_id=old_movie.cash_account,
                                                                category_id=old_movie.categories_id,
                                                                earning_id=old_movie.earnings_id,
                                                                type_operation=old_movie.type.value,
                                                                old_amount=old_movie.base_worth,
                                                                new_amount=new_worth)
                    # изменение движения по аккаунту
                    patch_data["base_worth"] = new_worth
                await self.repository.patch(session=session, data=patch_data,chat_id=token.id,
                                    table_id=user_movie.table_id)


    async def get_movies(self,user_movie: UserMoviesGet, token: JwtInfo) -> GenericResponse[UserMoviesRead]:
        async with self.session() as session:
            async with session.begin():
                result = await self.repository.find_paginated(session=session,page=user_movie.page, validate=True,
                                                              order_column="table_id", chat_id=token.id)
        result_movies = UserMoviesRead(movies=[])
        for i in result:
            result_movies.movies.append(UserMovieRead.model_validate(i, from_attributes=True))
        return GenericResponse[UserMoviesRead](detail=result_movies)


    async def get_movie(self, user_movie: UserMovieGet, token: JwtInfo) -> GenericResponse[UserMovieRead]:
        async with self.session() as session:
            result = await self.repository.find(session=session, validate=True, chat_id=token.id,
                            table_id=user_movie.table_id)
        result = UserMovieRead.model_validate(result, from_attributes=True)
        return GenericResponse[UserMovieRead](detail=result)

    async def delete_movie(self, user_movie: UserMovieGet, token: JwtInfo) -> None:
        async with self.session() as session:
            async with session.begin():
                # получение нужных таблиц
                old_movie: MovieOnAccount = await self.repository.find(session=session, validate=True,
                                                                       chat_id=token.id, table_id=user_movie.table_id)
                # удаление транзакции
                await self.repository.delete(session=session, chat_id=token.id, table_id=user_movie.table_id)
                # изменение баланса
                await self.work_with_money.delete_transaction(session=session,
                                                              chat_id=token.id,
                                                              cash_id=old_movie.cash_account,
                                                              category_id=old_movie.categories_id,
                                                              earning_id=old_movie.earnings_id,
                                                              type_operation=old_movie.type.value,
                                                              amount=old_movie.base_worth)
