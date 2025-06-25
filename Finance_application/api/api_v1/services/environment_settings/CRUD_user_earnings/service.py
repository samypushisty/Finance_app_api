from decimal import Decimal

from sqlalchemy import select, Result
from sqlalchemy.orm import joinedload, selectinload

from api.api_v1.services.environment_settings.CRUD_user_earnings.interface import UserEarningsServiceI
from api.api_v1.services.environment_settings.CRUD_user_earnings.schemas import UserTypeEarningsPost, \
    UserTypeEarningsPatch, UserTypesEarningsRead, UserTypeEarningsRead, UserTypeEarningsGet, UserTypeEarningsDelete
from api.api_v1.utils.repository import SQLAlchemyRepository
from api.api_v1.services.base_schemas.schemas import GenericResponse, StandartException
from api.api_v1.utils.work_with_money import WorkWithMoneyRepository
from core.models.base import Earnings
from secure import JwtInfo
from typing import Callable, Sequence
from sqlalchemy.ext.asyncio import AsyncSession


class UserEarningsService(UserEarningsServiceI):
    def __init__(self,
                 work_with_money: WorkWithMoneyRepository,
                 repository: SQLAlchemyRepository,
                 repository_movies: SQLAlchemyRepository,
                 database_session:Callable[..., AsyncSession]) -> None:
        self.repository = repository
        self.session = database_session
        self.work_with_money = work_with_money
        self.repository_movies = repository_movies

    async def post_user_type_of_earnings(self, user_type_of_earnings: UserTypeEarningsPost, token: JwtInfo) -> None:
        async with self.session() as session:
            async with session.begin():
                await self.repository.add(session=session,data={"chat_id": token.id, **user_type_of_earnings.model_dump()})


    async def patch_type_of_earnings(self, user_type_of_earnings: UserTypeEarningsPatch, token: JwtInfo) -> None:
        async with self.session() as session:
            async with session.begin():
                await self.repository.patch(session=session, data=user_type_of_earnings.model_dump(exclude_unset=True),
                                            chat_id=token.id, table_id=user_type_of_earnings.table_id)


    async def get_types_of_earnings(self, token: JwtInfo) -> GenericResponse[UserTypesEarningsRead]:
        async with self.session() as session:
            query = (
                select(Earnings)
                .options(selectinload(Earnings.currencies))
                .filter_by(chat_id=token.id)
                .order_by(Earnings.table_id)
            )
            types_of_earnings: Result = await session.execute(query)
            types_of_earnings: Sequence[Earnings] = types_of_earnings.scalars().all()
            if not types_of_earnings:
                raise StandartException(status_code=404, detail="not found")
        result_earnings = UserTypesEarningsRead(types_of_earnings=[])
        for type_of_earnings in types_of_earnings:
            balance = Decimal('0.00').quantize(Decimal('0.00'))
            for type_of_earnings_currency in type_of_earnings.currencies:
                balance += await self.work_with_money.convert(base_currency=type_of_earnings.currency,
                                                              convert_currency=type_of_earnings_currency.currency,
                                                              amount=type_of_earnings_currency.amount)
            response_data = UserTypeEarningsRead(
                table_id=type_of_earnings.table_id,
                chat_id=type_of_earnings.chat_id,
                name=type_of_earnings.name,
                description=type_of_earnings.description,
                currency=type_of_earnings.currency,
                balance=balance
            )
            result_earnings.types_of_earnings.append(response_data)
        return GenericResponse[UserTypesEarningsRead](detail=result_earnings)


    async def get_type_of_earnings(self, user_type_of_earnings: UserTypeEarningsGet, token: JwtInfo) -> GenericResponse[UserTypeEarningsRead]:
        async with self.session() as session:
            query = (select(Earnings).
                     options(joinedload(Earnings.currencies)).
                     filter_by(chat_id=token.id, table_id=user_type_of_earnings.table_id)
                     )
            type_of_earnings: Result = await session.execute(query)
            type_of_earnings: Earnings = type_of_earnings.scalars().first()
            if not type_of_earnings:
                raise StandartException(status_code=404, detail="not found")
        target_currency = type_of_earnings.currency
        if user_type_of_earnings.currency:
            target_currency = user_type_of_earnings.currency
        balance = Decimal('0.00').quantize(Decimal('0.00'))
        for type_of_earnings_currencies in type_of_earnings.currencies:
            balance += await self.work_with_money.convert(base_currency=target_currency,
                                                          convert_currency=type_of_earnings_currencies.currency,
                                                          amount=type_of_earnings_currencies.amount)
        response_data = UserTypeEarningsRead(
            table_id=type_of_earnings.table_id,
            chat_id=type_of_earnings.chat_id,
            name=type_of_earnings.name,
            description=type_of_earnings.description,
            currency=target_currency,
            balance=balance
        )
        return GenericResponse[UserTypeEarningsRead](detail=response_data)

    async def delete_type_of_earnings(self, user_type_of_earnings: UserTypeEarningsDelete, token: JwtInfo) -> None:
        async with self.session() as session:
            async with session.begin():
                await self.repository.delete(session=session, chat_id=token.id,table_id=user_type_of_earnings.table_id)
                await self.repository_movies.delete(session=session, validate=False, chat_id=token.id,earnings_id=user_type_of_earnings.table_id)
