from decimal import Decimal

from api.api_v1.services.environment_settings.CRUD_user_categories.interface import UserCategoriesServiceI
from api.api_v1.services.environment_settings.CRUD_user_categories.schemas import UserCategoryPost, \
    UserCategoryPatch, UserCategoriesRead, UserCategoryRead, UserCategoryGet
from api.api_v1.utils.repository import SQLAlchemyRepository
from api.api_v1.services.base_schemas.schemas import GenericResponse, StandartException
from api.api_v1.utils.work_with_money import WorkWithMoneyRepository
from secure import JwtInfo
from typing import Callable
from sqlalchemy.ext.asyncio import AsyncSession


class UserCategoriesService(UserCategoriesServiceI):
    def __init__(self,work_with_money: WorkWithMoneyRepository, repository: SQLAlchemyRepository, movies_repository: SQLAlchemyRepository,cash_account_repository: SQLAlchemyRepository, balance_repository: SQLAlchemyRepository, database_session:Callable[..., AsyncSession]) -> None:
        self.repository = repository
        self.repository_movies = movies_repository
        self.repository_cash_account = cash_account_repository
        self.repository_balance = balance_repository
        self.work_with_money = work_with_money
        self.session = database_session

    async def post_user_category(self, user_category: UserCategoryPost,
        token: JwtInfo) -> None:
        async with self.session() as session:
            async with session.begin():
                await self.repository.add(session=session,data={"chat_id": token.id, "balance": 0, **user_category.model_dump()})


    async def patch_user_category(self, user_category: UserCategoryPatch, token: JwtInfo) -> None:
        async with self.session() as session:
            async with session.begin():
                await self.repository.patch(session=session, data=user_category.model_dump(exclude_unset=True),
                                            chat_id=token.id, table_id=user_category.table_id)



    async def get_user_categories(self, token: JwtInfo) -> GenericResponse[UserCategoriesRead]:
        async with self.session() as session:
            result = await self.repository.find_all(session=session,order_column="table_id",chat_id=token.id)
        if not result:
            raise StandartException(status_code=404, detail="categories not found")
        result_categories = UserCategoriesRead(categories=[])
        for i in result:
            data = UserCategoryRead.model_validate(i, from_attributes=True)
            data.balance = await self.work_with_money.convert(base_currency=data.currency,
                                                              convert_currency="RUB",
                                                              amount=data.balance)
            result_categories.categories.append(data)
        return GenericResponse[UserCategoriesRead](detail=result_categories)


    async def get_user_category(self,user_category: UserCategoryGet, token: JwtInfo) -> GenericResponse[UserCategoryRead]:
        async with self.session() as session:
            result = await self.repository.find(session=session, chat_id=token.id,
                            table_id=user_category.table_id)
        if not result:
            raise StandartException(status_code=404, detail="category not found")
        if user_category.currency:
            result.currency = user_category.currency
        result = UserCategoryRead.model_validate(result, from_attributes=True)
        result.balance = await self.work_with_money.convert(base_currency=result.currency,
                                                            convert_currency="RUB",
                                                            amount=result.balance)
        return GenericResponse[UserCategoryRead](detail=result)


    async def delete_user_category(self,user_category: UserCategoryGet, token: JwtInfo) -> None:
        async with self.session() as session:
            async with session.begin():
                movies = await self.repository_movies.find_all(session=session, order_column="table_id", chat_id=token.id, categories_id=user_category.table_id)
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
                    main_balance += v
                    await self.repository_cash_account.patch_field(session=session, field="balance", value=v,
                                                      chat_id=token.id, table_id=k)
                await self.repository_balance.patch_field(session=session, field="balance", value=main_balance,
                                                          chat_id=token.id)

                await self.repository.delete(session=session, chat_id=token.id,table_id=user_category.table_id)
