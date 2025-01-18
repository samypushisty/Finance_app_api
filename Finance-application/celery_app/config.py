from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    BASE_URL: str = "http://0.0.0.0:8000"


# Создание экземпляра настроек
settings = Settings()


