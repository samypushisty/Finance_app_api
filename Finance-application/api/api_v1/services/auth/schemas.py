from pydantic import BaseModel, Field

class UserAuth(BaseModel):
    chat_id: int = Field(ge=10000000, le=10000000000)

class JWTRead(BaseModel):
    jwt: str