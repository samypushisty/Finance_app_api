from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        case_sensitive=False,
        env_nested_delimiter="__",
        env_prefix="CELERY_APP_CONFIG__",
        extra="ignore"
    )
    BASE_URL: str = "http://0.0.0.0:8000"
    API_key: str = None


# Создание экземпляра настроек
settings = Settings()


