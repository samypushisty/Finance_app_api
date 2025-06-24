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
        async with self.session() as session:
            async with session.begin():
                await self.repository.add(session=session, data={"chat_id": token.id,
                                                                 **user_movie.model_dump()})
                await self.work_with_money.add_transaction(session=session,
                                                           chat_id=token.id,
                                                           cash_id=user_movie.cash_account,
                                                           category_id=user_movie.categories_id,
                                                           earning_id=user_movie.earnings_id,
                                                           type_operation=user_movie.type,
                                                           currency=user_movie.currency,
                                                           amount=user_movie.worth)



    async def patch_movie(self, user_movie: UserMoviePatch, token: JwtInfo) -> None:
        async with self.session() as session:
            async with session.begin():
                patch_data = user_movie.model_dump(exclude_unset=True)
                if user_movie.worth or user_movie.currency:
                    # получение информации
                    old_movie: MovieOnAccount = await self.repository.find(session=session, validate=True,
                                                                           chat_id=token.id, table_id=user_movie.table_id)
                    if user_movie.currency:
                        new_currency = user_movie.currency
                    else:
                        new_currency = old_movie.currency

                    if user_movie.worth:
                        new_amount = user_movie.worth
                    else:
                        new_amount = old_movie.worth
                    await self.work_with_money.edit_transaction(session=session,
                                                                chat_id=token.id,
                                                                cash_id=old_movie.cash_account,
                                                                category_id=old_movie.categories_id,
                                                                earning_id=old_movie.earnings_id,
                                                                type_operation=old_movie.type.value,
                                                                new_amount=new_amount,
                                                                old_amount=old_movie.worth,
                                                                new_currency=new_currency,
                                                                old_currency=old_movie.currency)
                await self.repository.patch(session=session, data=patch_data,chat_id=token.id,
                                    table_id=user_movie.table_id)


    async def get_movies(self,user_movie: UserMoviesGet, token: JwtInfo) -> GenericResponse[UserMoviesRead]:
        additional_params = {}
        if user_movie.earnings_id is not None:
            additional_params["earnings_id"] = user_movie.earnings_id
        if user_movie.categories_id is not None:
            additional_params["categories_id"] = user_movie.categories_id
        if user_movie.cash_account_id is not None:
            additional_params["cash_account"] = user_movie.cash_account_id
        async with self.session() as session:
            async with session.begin():
                result = await self.repository.find_paginated(session=session,page=user_movie.page, validate=True,
                                                              order_column="table_id", chat_id=token.id, **additional_params)
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
