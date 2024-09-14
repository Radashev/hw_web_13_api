# from sqlalchemy import create_engine
# from sqlalchemy.orm import declarative_base, sessionmaker
# from typing import Generator
# import os
#
# # URL підключення до бази даних
# DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://postgres:567234@localhost:5438/postgres")
#
# # Створення двигуна для підключення до бази даних
# engine = create_engine(DATABASE_URL, echo=True)
#
# # Створення локального сеансу для роботи з базою даних
# SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
#
# # Базовий клас для оголошення моделей
# Base = declarative_base()
#
# # Dependency для отримання сеансу бази даних
# def get_db() -> Generator[SessionLocal, None, None]:
#     db = SessionLocal()
#     try:
#         yield db
#     finally:
#         db.close()


import os
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker
from typing import Generator

from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker

# Завантаження змінних середовища з файлу .env
load_dotenv()

# URL підключення до бази даних
DATABASE_URL = os.getenv("DATABASE_URL", "postgresql+asyncpg://postgres:567234@localhost:5438/postgres")
# DATABASE_URL = "postgresql+asyncpg://user:password@localhost/dbname"

# Створення двигуна для підключення до бази даних
engine = create_async_engine(DATABASE_URL, echo=True)

# Створення локального сеансу для роботи з базою даних
# SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine, class_=AsyncSession)
# Базовий клас для оголошення моделей
Base = declarative_base()


# Dependency для отримання сеансу бази даних
def get_db() -> Generator[SessionLocal, None, None]:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
