from abc import ABC, abstractmethod
from typing import Callable
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, update, delete

from api.api_v1.services.base_schemas.schemas import StandartException


class AbstractRepository(ABC):
    @abstractmethod
    async  def add(self, data: dict):
        ...

    @abstractmethod
    async def find(self,**filters):
        ...

    @abstractmethod
    async def find_all(self,order_column: str, **filters):
        ...

    @abstractmethod
    async def patch(self, data: dict, **filters):
        ...

    @abstractmethod
    async def delete(self,**filters):
        ...

class SQLAlchemyRepository(AbstractRepository):

    def __init__(self,model, session: Callable[..., AsyncSession]) -> None:
        self.session = session
        self.model = model

    async def add(self, data: dict):
        async with self.session() as session:
            async with session.begin():
                try:
                    stmt = self.model(**data)
                    session.add(stmt)
                    await session.commit()
                except:
                    await session.rollback()
                    raise StandartException(status_code=400, detail="Invalid data")


    async def find(self,**filters):
        async with self.session() as session:
            query = (
                select(self.model)
                .filter_by(**filters)
            )
            result = await session.execute(query)
            result = result.scalars().first()
            return result

    async def find_all(self,order_column: str, **filters):
        async with self.session() as session:
            query = (
                select(self.model)
                .filter_by(**filters)
                .order_by(getattr(self.model, order_column))
            )
            result = await session.execute(query)
            result = result.scalars().all()
            return result


    async def patch(self, data: dict, **filters):
        async with self.session() as session:
            async with session.begin():

                stmt = (
                    update(self.model)
                    .values(**data)
                    .filter_by(**filters)
                )
                try:
                    result = await session.execute(stmt)
                except:
                    raise StandartException(status_code=400, detail="Invalid data")
                if result.rowcount == 0:
                    await session.rollback()
                    raise StandartException(status_code=404, detail="not found")
                await session.commit()

    async def delete(self,**filters):
        async with self.session() as session:
            query = (
                delete(self.model)
                .filter_by(**filters)
            )
            result = await session.execute(query)
            if result.rowcount == 0:
                await session.rollback()
                raise StandartException(status_code=404, detail="not found")
            await session.commit()