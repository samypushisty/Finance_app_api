from api.api_v1.services.CRUD_Movie_on_account.interface import UserMovieServiceI
from api.api_v1.services.CRUD_Movie_on_account.schemas import UserMoviePost, UserMoviePatch, UserMoviesRead, \
    UserMovieRead, UserMovieGet
from api.api_v1.utils.work_with_money import WorkWithMoneyRepository
from api.api_v1.utils.repository import SQLAlchemyRepository
from api.api_v1.services.base_schemas.schemas import GenericResponse, StandartException
from core.models.base import CashAccount, MovieOnAccount, Balance
from secure import JwtInfo
from typing import Callable
from sqlalchemy.ext.asyncio import AsyncSession

class UserMovieService(UserMovieServiceI):
    def __init__(self,
                 work_with_money:WorkWithMoneyRepository,
                 repository: SQLAlchemyRepository,
                 repository_cash_account: SQLAlchemyRepository,
                 repository_balance: SQLAlchemyRepository,
                 database_session:Callable[..., AsyncSession]) -> None:
        self.work_with_money = work_with_money
        self.repository = repository
        self.repository_cash_account = repository_cash_account
        self.session = database_session
        self.repository_balance = repository_balance


    async def post_movie(self, user_movie: UserMoviePost, token: JwtInfo) -> None:
        async with self.session() as session:
            async with session.begin():
                # получение информации
                cash_account: CashAccount = await self.repository_cash_account.find(session=session, chat_id=token.id, cash_id=user_movie.cash_account)
                if not cash_account:
                    raise StandartException(status_code=404, detail="not found cash_account")
                main_account: Balance = await self.repository_balance.find(session=session, chat_id=token.id)

                # получение валют
                cash_account_currency: str = cash_account.currency
                movie_currency: str = user_movie.currency
                # конвертация денег
                cash_account_worth = await self.work_with_money.convert(base_currency=cash_account_currency,
                                                             convert_currency=movie_currency,
                                                             amount=user_movie.worth)
                main_account_worth = await self.work_with_money.convert(base_currency="RUB",
                                                             convert_currency=movie_currency,
                                                             amount=user_movie.worth)
                # добавление операции
                await self.repository.add(session=session, data={"chat_id": token.id, "cash_account_worth": cash_account_worth,
                                                                 "main_account_worth": main_account_worth,
                                                                 **user_movie.model_dump()})
                # изменение баланса кешаккаунта
                balance = await self.work_with_money.add_transaction(old_balance=cash_account.balance,
                                                               type_operation=user_movie.type,
                                                               amount=cash_account_worth)
                await self.repository_cash_account.patch(session=session,
                                                         data={"balance":balance},
                                                         chat_id=token.id,
                                                         cash_id=user_movie.cash_account)
                # изменение баланса всего аккаунта
                balance = await self.work_with_money.add_transaction(old_balance=main_account.total_balance,
                                                                     type_operation=user_movie.type,
                                                                     amount=main_account_worth)
                await self.repository_balance.patch(session=session,
                                                         data={"total_balance": balance},
                                                         chat_id=token.id)


    async def patch_movie(self, user_movie: UserMoviePatch, token: JwtInfo) -> None:
        async with self.session() as session:
            async with session.begin():
                patch_data = user_movie.model_dump(exclude_unset=True)
                if user_movie.currency or user_movie.worth:
                    # получение информации
                    old_movie: MovieOnAccount = await self.repository.find(session=session, chat_id=token.id,
                                                                           movie_id=user_movie.movie_id)
                    cash_account: CashAccount = await self.repository_cash_account.find(session=session,chat_id=token.id,
                                                                                        cash_id=old_movie.cash_account)
                    if not cash_account:
                        raise StandartException(status_code=404, detail="not found cash_account")
                    main_account: Balance = await self.repository_balance.find(session=session, chat_id=token.id)

                    # полуение валют
                    if not user_movie.currency:
                        movie_currency = old_movie.currency
                    else:
                        movie_currency = user_movie.currency
                    cash_account_currency: str = cash_account.currency

                    # получение старой стоймостей
                    if not user_movie.worth:
                        movie_worth = old_movie.worth
                    else:
                        movie_worth = user_movie.worth
                    old_cash_account_worth = old_movie.cash_account_worth
                    old_main_account_worth = old_movie.main_account_worth

                    # получение конвертированной стоймости кеш аккаунта
                    cash_account_worth = await self.work_with_money.convert(base_currency=cash_account_currency,
                                                             convert_currency=movie_currency,
                                                             amount=movie_worth)
                    # изменение баланса кеш аккаунта
                    balance = await self.work_with_money.edit_transaction(old_balance=cash_account.balance,
                                                                         type_operation=old_movie.type.value,
                                                                         old_amount=old_cash_account_worth,
                                                                         new_amount=cash_account_worth)
                    await self.repository_cash_account.patch(session=session,
                                                             data={"balance": balance},
                                                             chat_id=token.id,
                                                             cash_id=old_movie.cash_account)
                    # получение конвертированной стоймости общего аккаунта
                    main_account_worth = await self.work_with_money.convert(base_currency="RUB",
                                                                       convert_currency=movie_currency,
                                                                       amount=movie_worth)
                    # изменение баланса общего аккаунта
                    balance = await self.work_with_money.edit_transaction(old_balance=main_account.total_balance,
                                                                          type_operation=old_movie.type.value,
                                                                          old_amount=old_main_account_worth,
                                                                          new_amount=main_account_worth)
                    await self.repository_balance.patch(session=session,
                                                             data={"total_balance": balance},
                                                             chat_id=token.id,)
                    # изменение движения по аккаунту
                    patch_data["cash_account_worth"] = cash_account_worth
                    patch_data["main_account_worth"] = main_account_worth
                await self.repository.patch(session=session, data=patch_data,chat_id=token.id,
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
                # получение нужных таблиц
                old_movie: MovieOnAccount = await self.repository.find(session=session, chat_id=token.id,
                                                                       movie_id=user_movie.movie_id)
                cash_account: CashAccount = await self.repository_cash_account.find(session=session,
                                                                                    chat_id=token.id,
                                                                                    cash_id=old_movie.cash_account)
                if not cash_account:
                    raise StandartException(status_code=404, detail="not found cash_account")
                main_account: Balance = await self.repository_balance.find(session=session, chat_id=token.id)
                # получение старых стоймостей
                old_cash_account_worth = old_movie.cash_account_worth
                old_main_account_worth = old_movie.main_account_worth
                # изменение баланса кеш аккаунта
                balance = await self.work_with_money.delete_transaction(old_balance= cash_account.balance,
                                                                     type_operation=old_movie.type.value,
                                                                     amount=old_cash_account_worth)

                await self.repository_cash_account.patch(session=session,
                                                         data={"balance": balance},
                                                         chat_id=token.id,
                                                         cash_id=old_movie.cash_account)
                # изменение баланса главного аккаунта
                balance = await self.work_with_money.delete_transaction(old_balance=main_account.total_balance,
                                                                        type_operation=old_movie.type.value,
                                                                        amount=old_main_account_worth)

                await self.repository_balance.patch(session=session,
                                                         data={"total_balance": balance},
                                                         chat_id=token.id)
                await self.repository.delete(session=session,chat_id=token.id,movie_id=user_movie.movie_id)
