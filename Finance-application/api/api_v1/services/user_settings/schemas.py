from typing import Optional

from pydantic import BaseModel, Field, field_validator


from core.models.base import Theme, Language


class UserSettingsPatch(BaseModel):
    theme: Optional[Theme]
    language: Optional[Language]
    notifications: Optional[bool]
    main_currency: Optional[str] = Field(max_length=3)

    class Config:
        use_enum_values = True


class UserSettingsRead(BaseModel):
    chat_id: int = Field(ge=10000000, le=10000000000)
    theme: Theme
    language: Language
    notifications: bool
    main_currency: str = Field(max_length=3)

    class Config:
        validate_assignment = True
        use_enum_values = True

    @field_validator('language', mode='before')
    def validate_language(cls, value):
        if isinstance(value, Language):
            return Language(value).value
        return value

    @field_validator('theme', mode='before')
    def validate_theme(cls, value):
        if isinstance(value, Theme):
            return Theme(value).value
        return value