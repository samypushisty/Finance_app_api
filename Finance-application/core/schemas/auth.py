from pydantic import BaseModel, Field, field_validator
import re

class UserAuth(BaseModel):
    chat_id: int = Field(ge=10000000, le=10000000000)

class UserJWT(BaseModel):
    jwt: str

    @field_validator("jwt")
    @classmethod
    def validate_phone_number(cls, values: str) -> str:
        if not re.match(r'^[A-Za-z0-9-_]+\.[A-Za-z0-9-_]+\.[A-Za-z0-9-_]+$', values):
            raise ValueError('не джвт')
        return values