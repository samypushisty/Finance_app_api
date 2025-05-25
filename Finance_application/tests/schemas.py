from typing import Optional, Union

from pydantic import BaseModel

class DataDTO(BaseModel):
    status_code: int = 200
    data: Optional[dict] = None

class RequestDTO(BaseModel):
    token: str
    data: DataDTO

class DataForFixture(BaseModel):
    id: Union[str|int]
    data: DataDTO

