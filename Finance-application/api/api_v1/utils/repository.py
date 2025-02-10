from abc import ABC, abstractmethod
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, update, delete

from api.api_v1.services.base_schemas.schemas import StandartException


class AbstractRepository(ABC):
    @abstractmethod
    async  def add(self, session: AsyncSession, data: dict):
        ...

    @abstractmethod
    async def find(self, session: AsyncSession,**filters):
        ...

    @abstractmethod
    async def find_all(self, session: AsyncSession,order_column: str, **filters):
        ...

    @abstractmethod
    async def patch(self, session: AsyncSession, data: dict, **filters):
        ...

    @abstractmethod
    async def delete(self, session: AsyncSession,**filters):
        ...

class SQLAlchemyRepository(AbstractRepository):


    def __init__(self,model) -> None:
        self.model = model


    async def add(self, session: AsyncSession, data: dict):

        try:
            print("add")
            print(session)
            stmt = self.model(**data)
            session.add(stmt)
            await session.flush()
        except:

            raise StandartException(status_code=400, detail="Invalid data")


    async def find(self, session: AsyncSession,**filters):
        print("find")
        print(session)
        query = (
            select(self.model)
            .filter_by(**filters)
        )
        result = await session.execute(query)
        result = result.scalars().first()
        return result


    async def find_all(self, session: AsyncSession,order_column: str, **filters):
        print("find all")
        print(session)
        query = (
            select(self.model)
            .filter_by(**filters)
            .order_by(getattr(self.model, order_column))
        )
        result = await session.execute(query)
        result = result.scalars().all()
        return result


    async def patch(self, session: AsyncSession, data: dict, **filters):
        print("patch")
        print(session)
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
            raise StandartException(status_code=404, detail="not found")
        await session.flush()


    async def delete(self, session: AsyncSession,**filters):
        print("delete")
        print(session)
        query = (
            delete(self.model)
            .filter_by(**filters)
        )
        result = await session.execute(query)
        if result.rowcount == 0:
            raise StandartException(status_code=404, detail="not found")
        await session.flush()
