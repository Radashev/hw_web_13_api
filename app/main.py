import os
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from typing import List, Optional
from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from fastapi_jwt_auth import AuthJWT
from fastapi_jwt_auth.exceptions import AuthJWTException
from pydantic import BaseModel
from starlette.responses import JSONResponse
from passlib.context import CryptContext

from app.password_reset import router as password_reset_router
from app import models, schemas, crud
from app.db import get_db

# Завантаження змінних середовища
load_dotenv()

# Оновлення змінних середовища
DATABASE_URL = os.getenv('DATABASE_URL')
SECRET_KEY = os.getenv('JWT_SECRET_KEY')
print(f"SECRET_KEY: {SECRET_KEY}")

# Створення синхронного двигуна для створення таблиць
# sync_engine = create_engine(DATABASE_URL.replace('asyncpg', 'postgresql+psycopg2'))

# Створення бази даних
# models.Base.metadata.create_all(bind=sync_engine)

# Створення асинхронного двигуна
engine = create_async_engine(DATABASE_URL, echo=True)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine, class_=AsyncSession)

app = FastAPI()

app.include_router(password_reset_router)
# Налаштування шифрування паролів
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


# Налаштування для JWT
class Settings(BaseModel):
    authjwt_secret_key: str = SECRET_KEY
    authjwt_access_token_expires: int = 15  # in minutes
    authjwt_refresh_token_expires: int = 30  # in days


@AuthJWT.load_config
def get_config():
    return Settings()


@app.exception_handler(AuthJWTException)
def authjwt_exception_handler(request, exc):
    return JSONResponse(
        status_code=exc.status_code,
        content={"detail": exc.message}
    )


# Реєстрація нового користувача
@app.post("/register/", response_model=schemas.User)
def register(user: schemas.UserCreate, db: AsyncSession = Depends(get_db)):
    db_user = crud.get_user_by_email(db, email=user.email)
    if db_user:
        raise HTTPException(status_code=409, detail="Email already registered")
    hashed_password = pwd_context.hash(user.password)
    user_data = models.User(email=user.email, hashed_password=hashed_password)
    db.add(user_data)
    db.commit()
    db.refresh(user_data)
    return user_data


# Логін та отримання токенів
@app.post("/login/", response_model=schemas.Token)
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: AsyncSession = Depends(get_db),
          Authorize: AuthJWT = Depends()):
    db_user = crud.get_user_by_email(db, email=form_data.username)
    if not db_user or not pwd_context.verify(form_data.password, db_user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token = Authorize.create_access_token(subject=db_user.email)
    refresh_token = Authorize.create_refresh_token(subject=db_user.email)
    return {"access_token": access_token, "token_type": "bearer"}


# CRUD операції для контактів захищені JWT
@app.post("/contacts/", response_model=schemas.ContactOut)
def create_contact(contact: schemas.ContactCreate, db: AsyncSession = Depends(get_db), Authorize: AuthJWT = Depends()):
    Authorize.jwt_required()
    current_user = Authorize.get_jwt_subject()
    db_user = crud.get_user_by_email(db, email=current_user)
    return crud.create_contact(db=db, contact=contact, user_id=db_user.id)


@app.get("/contacts/", response_model=schemas.ContactList)
def read_contacts(skip: int = 0, limit: int = 10, name: Optional[str] = None, last_name: Optional[str] = None,
                  email: Optional[str] = None, db: AsyncSession = Depends(get_db), Authorize: AuthJWT = Depends()):
    Authorize.jwt_required()
    current_user = Authorize.get_jwt_subject()
    db_user = crud.get_user_by_email(db, email=current_user)
    contacts = crud.get_contacts(db=db, skip=skip, limit=limit, name=name, last_name=last_name, email=email,
                                 user_id=db_user.id)
    return schemas.ContactList(contacts=contacts)


@app.get("/contacts/{contact_id}", response_model=schemas.ContactOut)
def read_contact(contact_id: int, db: AsyncSession = Depends(get_db), Authorize: AuthJWT = Depends()):
    Authorize.jwt_required()
    current_user = Authorize.get_jwt_subject()
    db_user = crud.get_user_by_email(db, email=current_user)
    db_contact = crud.get_contact(db=db, contact_id=contact_id, user_id=db_user.id)
    if db_contact is None:
        raise HTTPException(status_code=404, detail="Contact not found")
    return db_contact


@app.put("/contacts/{contact_id}", response_model=schemas.ContactOut)
def update_contact(contact_id: int, contact: schemas.ContactUpdate, db: AsyncSession = Depends(get_db),
                   Authorize: AuthJWT = Depends()):
    Authorize.jwt_required()
    current_user = Authorize.get_jwt_subject()
    db_user = crud.get_user_by_email(db, email=current_user)
    db_contact = crud.update_contact(db=db, contact_id=contact_id, contact=contact, user_id=db_user.id)
    if db_contact is None:
        raise HTTPException(status_code=404, detail="Contact not found")
    return db_contact


@app.delete("/contacts/{contact_id}", response_model=schemas.ContactOut)
def delete_contact(contact_id: int, db: AsyncSession = Depends(get_db), Authorize: AuthJWT = Depends()):
    Authorize.jwt_required()
    current_user = Authorize.get_jwt_subject()
    db_user = crud.get_user_by_email(db, email=current_user)
    db_contact = crud.delete_contact(db=db, contact_id=contact_id, user_id=db_user.id)
    if db_contact is None:
        raise HTTPException(status_code=404, detail="Contact not found")
    return db_contact


@app.get("/contacts/upcoming_birthdays/", response_model=List[schemas.ContactOut])
def read_contacts_with_upcoming_birthdays(days: int = 7, db: AsyncSession = Depends(get_db),
                                          Authorize: AuthJWT = Depends()):
    Authorize.jwt_required()
    current_user = Authorize.get_jwt_subject()
    db_user = crud.get_user_by_email(db, email=current_user)
    return crud.get_contacts_with_upcoming_birthdays(db=db, user_id=db_user.id, days=days)
