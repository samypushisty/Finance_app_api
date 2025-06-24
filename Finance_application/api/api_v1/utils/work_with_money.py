from abc import ABC, abstractmethod
from decimal import Decimal, ROUND_HALF_UP
from typing import Callable, Literal

from redis.asyncio import Redis
from sqlalchemy import select, Result
from sqlalchemy.orm import joinedload
from api.api_v1.services.base_schemas.schemas import StandartException
from sqlalchemy.ext.asyncio import AsyncSession
from api.api_v1.utils.repository import SQLAlchemyRepository
from core.models.base import Category, CashAccount, CategoryCurrency, Earnings, EarningsCurrency
import logging

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)



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
                               new_amount: Decimal,
                               old_amount: Decimal,
                               new_currency: str,
                               old_currency: str,
                               type_operation: str):
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

        if type_operation == "outlay":
            query = (select(CashAccount).
                     options(joinedload(CashAccount.currencies_earnings)).
                     filter_by(table_id=cash_id, chat_id=chat_id)
                     )
            cash_table: Result = await session.execute(query)
            cash_table: CashAccount = cash_table.scalars().first()

            query = (select(Category).
                     options(joinedload(Category.currencies)).
                     filter_by(table_id=category_id, chat_id=chat_id)
                     )
            category_table: Result = await session.execute(query)
            category_table: Category = category_table.scalars().first()

            if not (category_table and cash_table):
                raise StandartException(status_code=404, detail="not_found")

            count_earning_currency = Decimal('0.00').quantize(Decimal('0.00'))
            for currencies_earning in cash_table.currencies_earnings:
                if currencies_earning.currency == currency:
                    count_earning_currency += currencies_earning.amount

            category_currency: CategoryCurrency = next((c for c in category_table.currencies if c.currency == currency), None)

            if count_earning_currency < amount:
                raise StandartException(status_code=403, detail="cash_balance_this_currency < 0")
            if not category_currency:
                category_table.currencies.append(
                    CategoryCurrency(chat_id=chat_id, cash_account_id=cash_id, currency=currency, amount=amount)
                )
            else:
                category_currency.amount += amount


        if type_operation == "earning":
            query = (select(Earnings).
                     options(joinedload(Earnings.currencies)).
                     filter_by(table_id=earning_id, chat_id=chat_id)
                     )
            earning_table: Result = await session.execute(query)
            earning_table: Earnings = earning_table.scalars().first()
            if not earning_table:
                raise StandartException(status_code=404, detail="not_found")

            earnings_currency: EarningsCurrency = next((c for c in earning_table.currencies if c.currency == currency), None)
            if not earnings_currency:
                earning_table.currencies.append(
                    EarningsCurrency(chat_id=chat_id, cash_account_id=cash_id, currency=currency, amount=amount)
                )
            else:
                earnings_currency.amount += amount


    async def edit_transaction(self, session: AsyncSession,
                               chat_id: int,
                               earning_id: int,
                               category_id: int,
                               cash_id: int,
                               new_amount: Decimal,
                               old_amount: Decimal,
                               new_currency: str,
                               old_currency: str,
                               type_operation: str):
        if type_operation == "earning":
            print(new_currency, new_amount, old_currency, old_amount)
            query = (select(CashAccount).
                     options(joinedload(CashAccount.currencies_earnings),
                             joinedload(CashAccount.currencies_outlays)).
                     filter_by(table_id=cash_id, chat_id=chat_id)
                     )
            cash_table: Result = await session.execute(query)
            cash_table: CashAccount = cash_table.scalars().first()

            count_old_outlay_currency = Decimal('0.00').quantize(Decimal('0.00'))
            for currencies_outlays in cash_table.currencies_outlays:
                if currencies_outlays.currency == old_currency:
                    count_old_outlay_currency+=currencies_outlays.amount
            print(count_old_outlay_currency)
            if not cash_table:
                raise StandartException(status_code=404, detail="not_found")

            earnings_currency_new: EarningsCurrency = next(
                (c for c in cash_table.currencies_earnings if c.currency == new_currency and c.earnings_id == earning_id), None)
            if not earnings_currency_new:
                print("создаём новый обьект")
                cash_table.currencies_earnings.append(
                    EarningsCurrency(chat_id=chat_id, earnings_id=earning_id, currency=new_currency, amount=new_amount)
                )
            else:
                print("добовляем к существующему")
                earnings_currency_new.amount += new_amount
                print(new_currency,earnings_currency_new.amount)
            if old_currency == new_currency:
                earnings_currency_old = earnings_currency_new
            else:
                earnings_currency_old: EarningsCurrency = next(
                    (c for c in cash_table.currencies_earnings if
                    c.currency == old_currency and c.earnings_id == earning_id), None)

            if earnings_currency_old.amount-old_amount < count_old_outlay_currency:
                raise StandartException(status_code=403, detail="cash_balance_this_currency < 0")
            else:
                earnings_currency_old.amount -= old_amount
                print(old_currency,earnings_currency_old.amount)
                if earnings_currency_old.amount == Decimal('0.00'):
                    await session.delete(earnings_currency_old)

        elif type_operation == "outlay":
            print(new_currency,new_amount,old_currency,old_amount)
            #таблица с кеш аккаунтами
            query = (select(CashAccount).
                     options(joinedload(CashAccount.currencies_earnings),
                             joinedload(CashAccount.currencies_outlays)).
                     filter_by(table_id=cash_id, chat_id=chat_id)
                     )
            cash_table: Result = await session.execute(query)
            cash_table: CashAccount = cash_table.scalars().first()

            #количство новой валюты в кеш аккаунте
            count_new_earning_currency = Decimal('0.00').quantize(Decimal('0.00'))
            for currencies_earning in cash_table.currencies_earnings:
                if currencies_earning.currency == new_currency:
                    count_new_earning_currency += currencies_earning.amount
            print(count_new_earning_currency)
            # если заработанной валюты такой нет значит я её потратить не могу
            if count_new_earning_currency == Decimal('0.00'):
                raise StandartException(status_code=403, detail="cash_balance_this_currency < 0")

            if not cash_table:
                raise StandartException(status_code=404, detail="not_found")

            #получение обьекта потраченной валюты
            category_new_currency: CategoryCurrency = next(
                (c for c in cash_table.currencies_outlays if c.currency == new_currency and c.category_id == category_id), None)


            if not category_new_currency:
                print("создаём новый обьект")
                cash_table.currencies_outlays.append(
                    CategoryCurrency(chat_id=chat_id, category_id=category_id, currency=new_currency, amount=new_amount)
                )
            else:
                print("добовляем к существующему")
                category_new_currency.amount += new_amount
                print(new_currency,category_new_currency.amount)
                # проверка на то что потаченных денег не больше заработанных
                if new_currency == old_currency:
                    if category_new_currency.amount-old_amount > count_new_earning_currency:
                        raise StandartException(status_code=403, detail="cash_balance_this_currency < 0")
                else:
                    if category_new_currency.amount > count_new_earning_currency:
                        raise StandartException(status_code=403, detail="cash_balance_this_currency < 0")

            if new_currency == old_currency:
                category_old_currency = category_new_currency
            else:
                category_old_currency: CategoryCurrency = next(
                    (c for c in cash_table.currencies_outlays if
                     c.currency == old_currency and c.category_id == category_id), None)

            category_old_currency.amount -= old_amount
            print(category_old_currency.amount)
            if category_old_currency.amount == Decimal('0.00'):
                print("удаляем старый")
                await session.delete(category_old_currency)


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
