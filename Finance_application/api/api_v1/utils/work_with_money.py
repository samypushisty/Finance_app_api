from abc import ABC, abstractmethod
from decimal import Decimal, ROUND_HALF_UP
from typing import Callable, Literal
from redis.asyncio import Redis
from sqlalchemy import select, Result
from sqlalchemy.orm import joinedload
from api.api_v1.services.base_schemas.schemas import StandartException
from sqlalchemy.ext.asyncio import AsyncSession
from api.api_v1.utils.repository import SQLAlchemyRepository
from core.models.base import Category, CashAccount, CashAccountCurrency, CategoryCurrency, Earnings, EarningsCurrency
import logging

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)

logger = logging.getLogger(__name__)



class AbstractConverter(ABC):
    @abstractmethod
    async  def convert(self, base_currency:str, convert_currency:str, amount:Decimal):
        ...

    @abstractmethod
    async def add_transaction(self, session: AsyncSession, chat_id: int,
                              earning_id: int,
                              category_id: int,
                              cash_id: int,
                              amount: Decimal,
                              currency: str,
                              type_operation: Literal["earning","outlay"]):
        ...

    @abstractmethod
    async def edit_transaction(self, session: AsyncSession,
                               chat_id: int,
                               earning_id: int,
                               category_id: int,
                               cash_id: int,
                               old_amount: Decimal,
                               new_amount: Decimal, type_operation: str):
        ...

    @abstractmethod
    async def delete_transaction(self, session: AsyncSession,
                                 chat_id: int,
                                 earning_id: int,
                                 category_id: int,
                                 cash_id: int,
                                 amount: Decimal,
                                 type_operation: Literal["earning", "outlay"]):
        ...


class WorkWithMoneyRepository(AbstractConverter):


    def __init__(self,db_redis: Callable[..., Redis],
                 repository_cash_account: SQLAlchemyRepository,
                 repository_balance: SQLAlchemyRepository,
                 repository_categories: SQLAlchemyRepository,
                 repository_type_of_earnings: SQLAlchemyRepository
                 ) -> None:
        self.db_redis = db_redis
        self.repository_cash_account = repository_cash_account
        self.repository_balance = repository_balance
        self.repository_categories = repository_categories
        self.repository_type_of_earnings = repository_type_of_earnings

    async def convert(self, base_currency:str, convert_currency:str, amount:Decimal):
        async with self.db_redis() as session:
            if base_currency == convert_currency:
                return amount
            price_base  = Decimal(await session.get(base_currency))
            price_convert = Decimal(await session.get(convert_currency))
        answer = (amount/price_convert*price_base).quantize(
                Decimal("0.00"),
                rounding=ROUND_HALF_UP)
        return answer

    async def add_transaction(self, session: AsyncSession,
                              chat_id: int,
                              earning_id: int,
                              category_id: int,
                              cash_id: int,
                              amount: Decimal,
                              currency: str,
                              type_operation: str):
        query = (select(CashAccount).
                 options(joinedload(CashAccount.currencies)).
                 filter_by(table_id=cash_id)
                 )
        cash_table: Result = await session.execute(query)
        cash_table: CashAccount = cash_table.scalars().first()
        logger.info("all currencies" + str(*[i.currency for i in cash_table.currencies]))

        if type_operation == "outlay":
            query = (select(Category).
                     options(joinedload(Category.currencies)).
                     filter_by(table_id=category_id)
                     )
            category_table: Result = await session.execute(query)
            category_table: Category = category_table.scalars().first()
            logger.info(*category_table.currencies)

            cash_currency: CashAccountCurrency = next((c for c in cash_table.currencies if c.currency == currency), None)
            category_currency: CategoryCurrency = next((c for c in category_table.currencies if c.currency == currency), None)

            if not cash_currency or cash_currency.amount < amount:
                raise StandartException(status_code=403, detail="cash_balance_this_currency < 0")
            else:
                cash_currency.amount -= amount

            if not category_currency:
                category_table.currencies.append(
                    CategoryCurrency(chat_id=chat_id, currency=currency, amount=amount)
                )
            else:
                category_currency.amount += amount

        if type_operation == "earning":
            query = (select(Earnings).
                     options(joinedload(Earnings.currencies)).
                     filter_by(table_id=earning_id)
                     )
            earning_table: Result = await session.execute(query)
            earning_table: Earnings = earning_table.scalars().first()
            logger.info("all currencies" + str(*[i.currency for i in earning_table.currencies]))

            cash_currency: CashAccountCurrency = next((c for c in cash_table.currencies if c.currency == currency), None)
            earnings_currency: EarningsCurrency = next((c for c in earning_table.currencies if c.currency == currency), None)

            if not cash_currency:
                cash_table.currencies.append(
                    CashAccountCurrency(chat_id=chat_id, currency=currency, amount=amount)
                )
            else:
                cash_currency.amount += amount

            if not earnings_currency:
                earning_table.currencies.append(
                    EarningsCurrency(chat_id=chat_id, currency=currency, amount=amount)
                )
            else:
                earnings_currency.amount += amount

    async def edit_transaction(self, session: AsyncSession,
                               chat_id: int,
                               earning_id: int,
                               category_id: int,
                               cash_id: int,
                               old_amount: Decimal,
                               new_amount: Decimal, type_operation: str):
        balance_cash_account = 0
        balance_main_account = 0
        if type_operation == "earning":
            balance_type_of_earnings = await self.repository_type_of_earnings.patch_field(session=session, field="balance",
                                                               value=(new_amount - old_amount),
                                                               chat_id=chat_id,table_id=earning_id)
            if balance_type_of_earnings < 0:
                raise StandartException(status_code=403, detail="type_of_earnings < 0")
            balance_cash_account = await self.repository_cash_account.patch_field(session=session, field="balance",
                                                               value=(new_amount - old_amount), chat_id=chat_id,
                                                               table_id=cash_id)
            balance_main_account = await self.repository_balance.patch_field(session=session, field="balance",
                                                               value=(new_amount - old_amount), chat_id=chat_id)
        elif type_operation == "outlay":
            balance_categories = await self.repository_categories.patch_field(session=session, field="balance",
                                                                              value=-(new_amount - old_amount), chat_id=chat_id,
                                                                              table_id=category_id)
            balance_cash_account = await self.repository_cash_account.patch_field(session=session, field="balance",
                                                                                  value=-(new_amount - old_amount),chat_id=chat_id,
                                                                                  table_id=cash_id)
            balance_main_account = await self.repository_balance.patch_field(session=session, field="balance",
                                                                             value=-(new_amount - old_amount), chat_id=chat_id)
            if balance_categories > 0:
                raise StandartException(status_code=403, detail="old_balance_categories > 0")
        if balance_main_account < 0 or balance_cash_account < 0:
            raise StandartException(status_code=403, detail="balance < 0")


    async def delete_transaction(self, session: AsyncSession,
                                 chat_id: int,
                                 earning_id: int,
                                 category_id: int,
                                 cash_id: int,
                                 amount: Decimal,type_operation: str):
        # получение нужных балансов
        balance_cash_account = 0
        balance_main_account = 0

        if type_operation == "earning":
            balance_type_of_earnings = await self.repository_type_of_earnings.patch_field(session=session,
                                                                                          field="balance",
                                                                                          value=-amount,
                                                                                          chat_id=chat_id,
                                                                                          table_id=earning_id)
            if balance_type_of_earnings < 0:
                raise StandartException(status_code=403, detail="type_of_earnings < 0")
            balance_cash_account = await self.repository_cash_account.patch_field(session=session, field="balance",
                                                                                  value=-amount,
                                                                                  chat_id=chat_id,
                                                                                  table_id=cash_id)
            balance_main_account = await self.repository_balance.patch_field(session=session, field="balance",
                                                                             value=-amount,
                                                                             chat_id=chat_id)
        elif type_operation == "outlay":
            balance_categories = await self.repository_categories.patch_field(session=session, field="balance",
                                                         value=amount, chat_id=chat_id,
                                                         table_id=category_id)
            balance_cash_account = await self.repository_cash_account.patch_field(session=session, field="balance",
                                                                                  value=amount, chat_id=chat_id,
                                                                                  table_id=cash_id)
            balance_main_account = await self.repository_balance.patch_field(session=session, field="balance",
                                                                             value=amount, chat_id=chat_id)
            if balance_categories > 0:
                raise StandartException(status_code=403, detail="old_balance_categories > 0")
        if balance_main_account < 0 or balance_cash_account < 0:
            raise StandartException(status_code=403, detail="balance < 0")
