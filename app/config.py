import os
from dotenv import load_dotenv
from pydantic import BaseSettings, Field

# Завантаження змінних середовища з файлу .env
load_dotenv()


class Settings(BaseSettings):
    DATABASE_URL: str = Field(..., env="DATABASE_URL")
    JWT_SECRET_KEY: str = Field(..., env="JWT_SECRET_KEY")
    JWT_ACCESS_TOKEN_EXPIRES: int = 15  # in minutes
    JWT_REFRESH_TOKEN_EXPIRES: int = 30  # in days
    SOME_OTHER_SETTING: str = "default_value"

    class Config:
        env_file = ".env"
        env_file_encoding = 'utf-8'


settings = Settings()

# Друк змінних середовища для перевірки
print(f"DATABASE_URL: {settings.DATABASE_URL}")
print(f"JWT_SECRET_KEY: {settings.JWT_SECRET_KEY}")
