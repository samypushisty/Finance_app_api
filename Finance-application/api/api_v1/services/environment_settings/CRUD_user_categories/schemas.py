from typing import  List, Optional

from pydantic import BaseModel, Field



class UserCategoryPost(BaseModel):
    month_limit: float = Field(ge=0)
    name: str = Field(max_length=15)

class UserCategoryPatch(BaseModel):
    category_id: Optional[int] = None
    month_limit: Optional[float] = Field(None, ge=0)
    name: Optional[str] = Field(None, max_length=15)

class UserCategoryGet(BaseModel):
    category_id: int


class UserCategoryRead(BaseModel):
    category_id: int
    chat_id: int = Field(ge=10000000, le=10000000000)
    month_limit: float = Field(ge=0)
    name: str = Field(max_length=15)

class UserCategoriesRead(BaseModel):
    categories: List[UserCategoryRead]
