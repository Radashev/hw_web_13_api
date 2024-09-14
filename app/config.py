import os
from pydantic import BaseSettings


class Settings(BaseSettings):
    # Налаштування бази даних
    DATABASE_URL: str = "postgresql://postgres:567234@localhost:5438/postgres"

    # Налаштування JWT
    JWT_SECRET_KEY: str = "your_secret_key"
    JWT_ACCESS_TOKEN_EXPIRES: int = 15  # in minutes
    JWT_REFRESH_TOKEN_EXPIRES: int = 30  # in days

    # Інші конфігураційні параметри
    SOME_OTHER_SETTING: str = "default_value"

    class Config:
        env_file = ".env"
        env_file_encoding = 'utf-8'


# Ініціалізація конфігурації
settings = Settings()
