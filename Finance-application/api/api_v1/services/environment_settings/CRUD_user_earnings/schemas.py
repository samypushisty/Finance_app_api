from typing import  List

from pydantic import BaseModel, Field



class UserTypeEarningsPost(BaseModel):
    name: str = Field(max_length=15)
    description: str = Field(max_length=256)


class UserTypeEarningsPatch(BaseModel):
    earning_id: int
    name: str = Field(max_length=15)
    description: str = Field(max_length=256)

class UserTypeEarningsGet(BaseModel):
    earning_id: int


class UserTypeEarningsRead(BaseModel):
    earning_id: int
    chat_id: int = Field(ge=10000000, le=10000000000)
    name: str = Field(max_length=15)
    description: str = Field(max_length=15)

class UserTypesEarningsRead(BaseModel):
    types_of_earnings: List[UserTypeEarningsRead]
