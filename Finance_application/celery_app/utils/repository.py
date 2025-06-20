from abc import ABC, abstractmethod
from typing import List

from sqlalchemy.orm import Session
from sqlalchemy import select


class AbstractRepository(ABC):
    pass

class SQLAlchemyRepository(AbstractRepository):


    def __init__(self,model) -> None:
        self.model = model

