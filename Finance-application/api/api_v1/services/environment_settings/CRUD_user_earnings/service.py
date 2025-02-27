from decimal import Decimal

from api.api_v1.services.environment_settings.CRUD_user_earnings.interface import UserEarningsServiceI
from api.api_v1.services.environment_settings.CRUD_user_earnings.schemas import UserTypeEarningsPost, \
    UserTypeEarningsPatch, UserTypesEarningsRead, UserTypeEarningsRead, UserTypeEarningsGet
from api.api_v1.utils.repository import SQLAlchemyRepository
from api.api_v1.services.base_schemas.schemas import GenericResponse, StandartException
from api.api_v1.utils.work_with_money import WorkWithMoneyRepository
from secure import JwtInfo
from typing import Callable
from sqlalchemy.ext.asyncio import AsyncSession


class UserEarningsService(UserEarningsServiceI):
    def __init__(self,work_with_money: WorkWithMoneyRepository, repository: SQLAlchemyRepository, movies_repository: SQLAlchemyRepository, balance_repository: SQLAlchemyRepository,cash_account_repository: SQLAlchemyRepository, database_session:Callable[..., AsyncSession]) -> None:
        self.repository = repository
        self.repository_movies = movies_repository
        self.session = database_session
        self.repository_cash_account = cash_account_repository
        self.repository_balance = balance_repository
        self.work_with_money = work_with_money

    async def post_user_type_of_earnings(self, user_type_of_earnings: UserTypeEarningsPost, token: JwtInfo) -> None:
        async with self.session() as session:
            async with session.begin():
                await self.repository.add(session=session,data={"chat_id": token.id,"balance": 0, **user_type_of_earnings.model_dump()})


    async def patch_type_of_earnings(self, user_type_of_earnings: UserTypeEarningsPatch, token: JwtInfo) -> None:
        async with self.session() as session:
            async with session.begin():
                await self.repository.patch(session=session, data=user_type_of_earnings.model_dump(exclude_unset=True),
                                            chat_id=token.id, table_id=user_type_of_earnings.table_id)


    async def get_types_of_earnings(self, token: JwtInfo) -> GenericResponse[UserTypesEarningsRead]:
        async with self.session() as session:
            result = await self.repository.find_all(session=session,order_column="table_id",chat_id=token.id)
        if not result:
            raise StandartException(status_code=404, detail="types of earnings not found")
        result_types = UserTypesEarningsRead(types_of_earnings=[])
        for i in result:

            data = UserTypeEarningsRead.model_validate(i, from_attributes=True)
            data.balance = await self.work_with_money.convert(base_currency=data.currency,
                                                              convert_currency="RUB",
                                                              amount=data.balance)
            result_types.types_of_earnings.append(data)
        return GenericResponse[UserTypesEarningsRead](detail=result_types)


    async def get_type_of_earnings(self, user_type_of_earnings: UserTypeEarningsGet, token: JwtInfo) -> GenericResponse[UserTypeEarningsRead]:
        async with self.session() as session:
            result = await self.repository.find(session=session, chat_id=token.id,
                            table_id=user_type_of_earnings.table_id)
        if not result:
            raise StandartException(status_code=404, detail="type of earnings not found")
        result = UserTypeEarningsRead.model_validate(result, from_attributes=True)
        result.balance = await self.work_with_money.convert(base_currency=result.currency,
                                                            convert_currency="RUB",
                                                            amount=result.balance)
        return GenericResponse[UserTypeEarningsRead](detail=result)

    async def delete_type_of_earnings(self, user_type_of_earnings: UserTypeEarningsGet, token: JwtInfo) -> None:
        async with self.session() as session:
            async with session.begin():
                movies = await self.repository_movies.find_all(session=session, order_column="table_id",
                                                               chat_id=token.id, earnings_id=user_type_of_earnings.table_id)
                cash_accounts_balance = {}
                id_cash_account = 0
                worth = 0
                for i in movies:
                    id_cash_account = i.cash_account
                    worth = i.base_worth
                    if not id_cash_account in cash_accounts_balance:
                        cash_accounts_balance[id_cash_account] = worth
                    else:
                        cash_accounts_balance[id_cash_account] += worth
                main_balance = Decimal("0.00")
                for k, v in cash_accounts_balance.items():
                    balance = await self.repository_cash_account.patch_field(session=session, field="balance", value=-v,
                                                                   chat_id=token.id, table_id=k)
                    main_balance += v
                    if balance < 0:
                        raise StandartException(status_code=404, detail="balance < 0")
                await self.repository_balance.patch_field(session=session, field="balance", value=-main_balance,
                                                                   chat_id=token.id)

                await self.repository.delete(session=session, chat_id=token.id,table_id=user_type_of_earnings.table_id)

