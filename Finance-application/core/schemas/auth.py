from pydantic import BaseModel, Field

class UserAuth(BaseModel):
    chat_id: int = Field(ge=10000000, le=10000000000)

class UserRegistration(BaseModel):
    chat_id: int = Field(ge=10000000, le=10000000000)
    currencies: str
    type_of_earnings: str