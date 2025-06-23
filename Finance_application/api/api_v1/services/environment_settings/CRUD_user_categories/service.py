from decimal import Decimal

from sqlalchemy import select, Result
from sqlalchemy.orm import joinedload, selectinload

from api.api_v1.services.environment_settings.CRUD_user_categories.interface import UserCategoriesServiceI
from api.api_v1.services.environment_settings.CRUD_user_categories.schemas import UserCategoryPost, \
    UserCategoryPatch, UserCategoriesRead, UserCategoryRead, UserCategoryGet, UserCategoryDelete
from api.api_v1.utils.repository import SQLAlchemyRepository
from api.api_v1.services.base_schemas.schemas import GenericResponse, StandartException
from api.api_v1.utils.work_with_money import WorkWithMoneyRepository
from core.models.base import Category
from secure import JwtInfo
from typing import Callable, Sequence
from sqlalchemy.ext.asyncio import AsyncSession


class UserCategoriesService(UserCategoriesServiceI):
    def __init__(self,
                 work_with_money: WorkWithMoneyRepository,
                 repository: SQLAlchemyRepository,
                 movies_repository: SQLAlchemyRepository,
                 database_session:Callable[..., AsyncSession]) -> None:
        self.repository = repository
        self.repository_movies = movies_repository
        self.work_with_money = work_with_money
        self.session = database_session

    async def post_user_category(self, user_category: UserCategoryPost,
        token: JwtInfo) -> None:
        async with self.session() as session:
            async with session.begin():
                await self.repository.add(session=session,data={"chat_id": token.id, **user_category.model_dump()})


    async def patch_user_category(self, user_category: UserCategoryPatch, token: JwtInfo) -> None:
        async with self.session() as session:
            async with session.begin():
                await self.repository.patch(session=session, data=user_category.model_dump(exclude_unset=True),
                                            chat_id=token.id, table_id=user_category.table_id)



    async def get_user_categories(self, token: JwtInfo) -> GenericResponse[UserCategoriesRead]:
        async with self.session() as session:
            query = (
                select(Category)
                .options(selectinload(Category.currencies))
                .filter_by(chat_id=token.id)
                .order_by(Category.table_id)
            )
            categories: Result = await session.execute(query)
            categories: Sequence[Category] = categories.scalars().all()
            if not categories:
                raise StandartException(status_code=404, detail="not found")
        result_categories = UserCategoriesRead(categories=[])
        for category in categories:
            balance = Decimal('0.00').quantize(Decimal('0.00'))
            for category_currency in category.currencies:
                balance += await self.work_with_money.convert(base_currency=category_currency.currency,
                                                              convert_currency=category_currency.currency,
                                                              amount=category_currency.amount)
            response_data = UserCategoryRead(
            table_id=category.table_id,
            chat_id=category.chat_id,
            name=category.name,
            description=category.description,
            month_limit=category.month_limit,
            currency=category.currency,
            balance=balance
            )
            result_categories.categories.append(response_data)
        return GenericResponse[UserCategoriesRead](detail=result_categories)


    async def get_user_category(self,user_category: UserCategoryGet, token: JwtInfo) -> GenericResponse[UserCategoryRead]:
        async with self.session() as session:
            query = (select(Category).
                     options(joinedload(Category.currencies)).
                     filter_by(chat_id=token.id, table_id=user_category.table_id)
                     )
            category: Result = await session.execute(query)
            category: Category = category.scalars().first()
            if not category:
                raise StandartException(status_code=404, detail="not found")
        target_currency = category.currency
        if user_category.currency:
            target_currency = user_category.currency
        balance = Decimal('0.00').quantize(Decimal('0.00'))
        for category_currencies in category.currencies:
            balance += await self.work_with_money.convert(base_currency=target_currency,
                                                          convert_currency=category_currencies.currency,
                                                          amount=category_currencies.amount)
        response_data = UserCategoryRead(
            table_id=category.table_id,
            chat_id=category.chat_id,
            name=category.name,
            description=category.description,
            month_limit=category.month_limit,
            currency=target_currency,
            balance=balance
        )
        return GenericResponse[UserCategoryRead](detail=response_data)


    async def delete_user_category(self,user_category: UserCategoryDelete, token: JwtInfo) -> None:
        async with self.session() as session:
            async with session.begin():
                await self.repository.delete(session=session, chat_id=token.id,table_id=user_category.table_id)
                await self.repository_movies.delete(session=session, validate=False, chat_id=token.id, earnings_id=user_category.table_id)
