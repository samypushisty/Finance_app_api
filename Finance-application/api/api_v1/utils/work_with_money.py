from abc import ABC, abstractmethod
from decimal import Decimal, ROUND_HALF_UP
from typing import Callable, Literal
from redis.asyncio import Redis
from api.api_v1.services.base_schemas.schemas import StandartException
from sqlalchemy.ext.asyncio import AsyncSession

from api.api_v1.utils.repository import SQLAlchemyRepository
from core.models.base import CashAccount, Balance, Category, Earnings


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
                              type_operation: str):
        # получение нужных таблиц
        cash_account: CashAccount = await self.repository_cash_account.find(session=session, chat_id=chat_id,
                                                                            table_id=cash_id)
        categories: Category = await self.repository_categories.find(session=session, chat_id=chat_id,
                                                                            table_id=category_id)
        type_of_earnings: Earnings = await self.repository_type_of_earnings.find(session=session, chat_id=chat_id,
                                                                            table_id=earning_id)
        main_account: Balance = await self.repository_balance.find(session=session, chat_id=chat_id)

        # получение нужных балансов
        old_balance_cash_account = getattr(cash_account, "balance", None)
        old_balance_main_account = getattr(main_account, "balance", None)



        # изменение балансов
        if type_operation == "outlay":
            old_balance_categories = getattr(categories, "balance", None)
            print(amount)
            old_balance_cash_account -= amount
            old_balance_categories  -= amount
            old_balance_main_account -= amount
            if old_balance_cash_account < 0 or old_balance_main_account < 0:
                raise StandartException(status_code=403, detail="balance < 0")
            await self.repository_categories.patch(session=session,
                                                   data={"balance": old_balance_categories},
                                                   chat_id=chat_id, table_id=category_id)
        elif type_operation == "earning":
            old_balance_type_of_earnings = getattr(type_of_earnings, "balance", None)
            old_balance_cash_account += amount
            old_balance_main_account += amount
            old_balance_type_of_earnings += amount
            await self.repository_type_of_earnings.patch(session=session,
                                                         data={"balance": old_balance_type_of_earnings},
                                                         chat_id=chat_id, table_id=earning_id)

        # применение балансов
        await self.repository_cash_account.patch(session=session,
                                            data={"balance": old_balance_cash_account},
                                            chat_id=chat_id, table_id=cash_id)

        await self.repository_balance.patch(session=session,
                                                 data={"balance": old_balance_main_account},
                                                 chat_id=chat_id)

    async def edit_transaction(self, session: AsyncSession,
                               chat_id: int,
                               earning_id: int,
                               category_id: int,
                               cash_id: int,
                               old_amount: Decimal,
                               new_amount: Decimal, type_operation: str):
        # получение нужных таблиц
        cash_account: CashAccount = await self.repository_cash_account.find(session=session, chat_id=chat_id,
                                                                            table_id=cash_id)
        categories: Category = await self.repository_categories.find(session=session, chat_id=chat_id,
                                                                     table_id=category_id)
        type_of_earnings: Earnings = await self.repository_type_of_earnings.find(session=session, chat_id=chat_id,
                                                                                 table_id=earning_id)
        main_account: Balance = await self.repository_balance.find(session=session, chat_id=chat_id)

        # получение нужных балансов
        old_balance_cash_account = cash_account.balance
        old_balance_main_account = main_account.balance
        print(old_balance_cash_account, old_balance_main_account)

        if type_operation == "earning":
            old_balance_type_of_earnings = type_of_earnings.balance
            old_balance_cash_account += new_amount - old_amount
            old_balance_main_account += new_amount - old_amount
            old_balance_type_of_earnings += new_amount - old_amount
            if old_balance_type_of_earnings < 0:
                raise StandartException(status_code=403, detail="type_of_earnings < 0")
            await self.repository_type_of_earnings.patch(session=session,
                                                         data={"balance": old_balance_type_of_earnings},
                                                         chat_id=chat_id, table_id=earning_id)
        elif type_operation == "outlay":
            old_balance_categories = categories.balance
            old_balance_cash_account -= new_amount - old_amount
            old_balance_categories -= new_amount - old_amount
            old_balance_main_account -= new_amount - old_amount
            print(old_balance_cash_account, old_balance_categories, old_balance_main_account)
            if old_balance_categories > 0:
                raise StandartException(status_code=403, detail="old_balance_categories > 0")
            await self.repository_categories.patch(session=session,
                                                   data={"balance": old_balance_categories},
                                                   chat_id=chat_id, table_id=category_id)
        if old_balance_main_account < 0 or old_balance_cash_account < 0:
            raise StandartException(status_code=403, detail="balance < 0")

        # применение балансов
        await self.repository_cash_account.patch(session=session,
                                                 data={"balance": old_balance_cash_account},
                                                 chat_id=chat_id, table_id=cash_id)
        await self.repository_balance.patch(session=session,
                                            data={"balance": old_balance_main_account},
                                            chat_id=chat_id)

    async def delete_transaction(self, session: AsyncSession,
                                 chat_id: int,
                                 earning_id: int,
                                 category_id: int,
                                 cash_id: int,
                                 amount: Decimal,type_operation: str):
        # получение нужных таблиц
        cash_account: CashAccount = await self.repository_cash_account.find(session=session, chat_id=chat_id,
                                                                            table_id=cash_id)
        categories: Category = await self.repository_categories.find(session=session, chat_id=chat_id,
                                                                     table_id=category_id)
        type_of_earnings: Earnings = await self.repository_type_of_earnings.find(session=session, chat_id=chat_id,
                                                                                 table_id=earning_id)
        main_account: Balance = await self.repository_balance.find(session=session, chat_id=chat_id)

        # получение нужных балансов
        old_balance_cash_account = cash_account.balance
        old_balance_main_account = main_account.balance

        if type_operation == "earning":
            old_balance_type_of_earnings = type_of_earnings.balance
            old_balance_cash_account -= amount
            old_balance_main_account -= amount
            old_balance_type_of_earnings -= amount
            if old_balance_type_of_earnings < 0:
                raise StandartException(status_code=403, detail="type_of_earnings < 0")
            await self.repository_type_of_earnings.patch(session=session,
                                                         data={"balance": old_balance_type_of_earnings},
                                                         chat_id=chat_id, table_id=earning_id)
        elif type_operation == "outlay":
            old_balance_categories = categories.balance
            old_balance_cash_account += amount
            old_balance_categories += amount
            old_balance_main_account += amount
            if old_balance_categories > 0:
                raise StandartException(status_code=403, detail="old_balance_categories > 0")
            await self.repository_categories.patch(session=session,
                                                   data={"balance": old_balance_categories},
                                                   chat_id=chat_id, table_id=category_id)
        if old_balance_main_account < 0 or old_balance_cash_account < 0:
            raise StandartException(status_code=403, detail="balance < 0")

        # применение балансов
        await self.repository_cash_account.patch(session=session,
                                                 data={"balance": old_balance_cash_account},
                                                 chat_id=chat_id, table_id=cash_id)


        await self.repository_balance.patch(session=session,
                                            data={"balance": old_balance_main_account},
                                            chat_id=chat_id)