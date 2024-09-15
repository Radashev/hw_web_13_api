from typing import AsyncGenerator, Generator

import os
from pathlib import Path
from dotenv import load_dotenv
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker, declarative_base
from pydantic import BaseSettings

# # Завантаження змінних середовища з файлу .env
# load_dotenv()

# Завантаження змінних середовища з файлу .env
env_path = Path('.') / '.env'
load_dotenv(dotenv_path=env_path)

# Перевірка змінних середовища
database_url = os.getenv("DATABASE_URL")
secret_key = os.getenv("JWT_SECRET_KEY")

print(f"DATABASE_URL: {database_url}")
print(f"SECRET_KEY: {secret_key}")


class Settings(BaseSettings):
    DATABASE_URL: str

    class Config:
        env_file = ".env"
        env_file_encoding = 'utf-8'


settings = Settings()

# Створення асинхронного двигуна для підключення до бази даних
engine = create_async_engine(settings.DATABASE_URL, echo=True)

# Створення асинхронного сеансу для роботи з базою даних
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine, class_=AsyncSession)

# Базовий клас для оголошення моделей
Base = declarative_base()


# Dependency для отримання асинхронного сеансу бази даних
async def get_db() -> AsyncGenerator[AsyncSession, None]:
    async with SessionLocal() as db:
        yield db
