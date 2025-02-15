from decimal import Decimal
from locale import currency

from api.api_v1.services.CRUD_Movie_on_account.interface import UserMovieServiceI
from api.api_v1.services.CRUD_Movie_on_account.schemas import UserMoviePost, UserMoviePatch, UserMoviesRead, \
    UserMovieRead, UserMovieGet
from api.api_v1.utils.converter import ConverterRepository
from api.api_v1.utils.repository import SQLAlchemyRepository
from api.api_v1.services.base_schemas.schemas import GenericResponse, StandartException
from core.models.base import CashAccount, MovieOnAccount
from secure import JwtInfo
from typing import Callable
from sqlalchemy.ext.asyncio import AsyncSession

class UserMovieService(UserMovieServiceI):
    def __init__(self, converter: ConverterRepository, repository: SQLAlchemyRepository, repository_cash_account: SQLAlchemyRepository, database_session:Callable[..., AsyncSession]) -> None:
        self.converter = converter
        self.repository = repository
        self.repository_cash_account = repository_cash_account
        self.session = database_session

    async def post_movie(self, user_movie: UserMoviePost, token: JwtInfo) -> None:
        async with self.session() as session:
            async with session.begin():
                cash_account: CashAccount = await self.repository_cash_account.find(session=session, chat_id=token.id, cash_id=user_movie.cash_account)
                base_currency: str = cash_account.currency
                balance: Decimal = cash_account.balance
                worth_in_base = await self.converter.convert(base_currency=base_currency, convert_currency=user_movie.currency, amount=user_movie.worth)
                print(type(worth_in_base))
                await self.repository.add(session=session, data={"chat_id": token.id,"base_worth":worth_in_base, **user_movie.model_dump()})
                if user_movie.type == "outlay":
                    balance -= worth_in_base
                    if balance < 0:
                        raise StandartException(status_code=403, detail="balance < 0")

                elif user_movie.type == "earning":
                    balance += worth_in_base
                await self.repository_cash_account.patch(session=session,
                                                         data={"balance":balance},
                                                         chat_id=token.id,
                                                         cash_id=user_movie.cash_account)


    async def patch_movie(self, user_movie: UserMoviePatch, token: JwtInfo) -> None:
        async with self.session() as session:
            async with session.begin():
                patch_data = user_movie.model_dump()
                if user_movie.currency or user_movie.worth:
                    print("change balnce")
                    # получение старого движения по аккаунту
                    old_movie: MovieOnAccount = await self.repository.find(session=session, chat_id=token.id, movie_id=user_movie.movie_id)
                    cash_account: CashAccount = await self.repository_cash_account.find(session=session,
                                                                                        chat_id=token.id,
                                                                                        cash_id=old_movie.cash_account)

                    # проверки есть ли валюта или количество
                    if not user_movie.currency:
                        movie_currency = old_movie.currency
                    else:
                        movie_currency = user_movie.currency
                    if not user_movie.worth:
                        movie_worth = old_movie.worth
                    else:
                        movie_worth = user_movie.worth

                    # получение нужных цифр

                    old_worth = old_movie.base_worth
                    base_currency: str = cash_account.currency

                    print(base_currency,movie_currency,movie_worth)
                    # получение конвертированной суммы
                    worth_in_base = await self.converter.convert(base_currency=base_currency,
                                                             convert_currency=movie_currency,
                                                             amount=movie_worth)
                    # изменение баланса
                    balance: Decimal = cash_account.balance
                    balance -= old_worth
                    balance += worth_in_base
                    if balance < 0:
                        raise StandartException(status_code=403, detail="balance < 0")
                    await self.repository_cash_account.patch(session=session,
                                                             data={"balance": balance},
                                                             chat_id=token.id,
                                                             cash_id=old_movie.cash_account)
                    # изменение баззовой суммы
                    patch_data["base_worth"] = worth_in_base
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
                # изменение баланса
                old_worth = old_movie.base_worth
                balance: Decimal = cash_account.balance
                if old_movie.type.value == "earning":
                    balance -= old_worth
                else:
                    balance += old_worth
                await self.repository_cash_account.patch(session=session,
                                                         data={"balance": balance},
                                                         chat_id=token.id,
                                                         cash_id=old_movie.cash_account)
                await self.repository.delete(session=session,chat_id=token.id,movie_id=user_movie.movie_id)
