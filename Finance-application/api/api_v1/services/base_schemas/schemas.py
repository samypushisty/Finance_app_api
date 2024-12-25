from pydantic import BaseModel
from typing import Generic, TypeVar, Optional
T = TypeVar('T')


class GenericResponse(BaseModel, Generic[T]):
    status_code: int = 200
    detail: Optional[T] = None