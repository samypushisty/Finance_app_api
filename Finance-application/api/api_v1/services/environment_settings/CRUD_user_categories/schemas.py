from typing import  List

from pydantic import BaseModel, Field



class UserCategoryPost(BaseModel):
    month_limit: float
    name: str = Field(max_length=15)

class UserCategoryPatch(BaseModel):
    category_id: int
    month_limit: float
    name: str = Field(max_length=15)

class UserCategoryGet(BaseModel):
    category_id: int


class UserCategoryRead(BaseModel):
    category_id: int
    chat_id: int = Field(ge=10000000, le=10000000000)
    month_limit: float
    name: str = Field(max_length=15)

class UserCategoriesRead(BaseModel):
    categories: List[UserCategoryRead]
