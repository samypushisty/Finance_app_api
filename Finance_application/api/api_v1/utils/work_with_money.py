from abc import ABC, abstractmethod
from decimal import Decimal, ROUND_HALF_UP
from typing import Callable, Literal
from redis.asyncio import Redis
from api.api_v1.services.base_schemas.schemas import StandartException
from sqlalchemy.ext.asyncio import AsyncSession

from api.api_v1.utils.repository import SQLAlchemyRepository


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
        # изменение балансов
        if type_operation == "outlay":
            await self.repository_categories.patch_field(session=session, field="balance",
                                                                              value=-amount,chat_id=chat_id,
                                                                              table_id=category_id)
            balance_cash_account = await self.repository_cash_account.patch_field(session=session, field="balance",
                                                                                  value=-amount,chat_id=chat_id,
                                                                                  table_id=cash_id)
            balance_main_account = await self.repository_balance.patch_field(session=session, field="balance",
                                                                             value=-amount,chat_id=chat_id)
            if balance_cash_account < 0 or balance_main_account < 0:
                raise StandartException(status_code=403, detail="balance < 0")
        elif type_operation == "earning":
            await self.repository_type_of_earnings.patch_field(session=session,field="balance",
                                                               value=amount,chat_id=chat_id,
                                                               table_id=earning_id)
            await self.repository_cash_account.patch_field(session=session, field="balance",
                                                           value=amount,chat_id=chat_id,
                                                           table_id=cash_id)
            await self.repository_balance.patch_field(session=session, field="balance",
                                                      value=amount,chat_id=chat_id)


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
