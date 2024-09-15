import os
from pydantic import BaseSettings
from app.config import Settings


class Settings(BaseSettings):
    DATABASE_URL: str
    SECRET_KEY: str
    PASSWORD_RESET_SECRET_KEY: str
    PASSWORD_RESET_TOKEN_EXPIRES: int

    class Config:
        env_file = ".env"
        env_file_encoding = 'utf-8'


settings = Settings()
