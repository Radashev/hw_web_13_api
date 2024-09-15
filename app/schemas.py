from pydantic import BaseModel, Field, validator, root_validator
from typing import List, Optional
from datetime import date


class User(BaseModel):
    email: str
    id: int


class UserCreate(BaseModel):
    email: str
    password: str


class Token(BaseModel):
    access_token: str
    token_type: str


class ContactBase(BaseModel):
    first_name: str
    last_name: str
    email: str
    phone: str
    birthday: date
    additional_info: Optional[str] = None

    @root_validator(pre=True)
    def validate_all(cls, values):
        birthday = values.get('birthday')
        if birthday and birthday > date.today():
            raise ValueError('Birthday cannot be in the future')
        return values


class ContactCreate(BaseModel):
    name: str
    last_name: str
    email: str
    phone: str


class ContactUpdate(BaseModel):
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    email: Optional[str] = None
    phone: Optional[str] = None
    birthday: Optional[date] = None
    additional_info: Optional[str] = None

    @validator('birthday')
    def validate_birthday(cls, v):
        if v and v > date.today():
            raise ValueError('Birthday cannot be in the future')
        return v


class ContactOut(ContactBase):
    id: int

    class Config:
        from_attributes = True  # Замість 'orm_mode'


class ContactList(BaseModel):
    contacts: List[ContactOut]

    @validator('contacts')
    def validate_contacts(cls, v):
        for contact in v:
            if contact.id <= 0:
                raise ValueError('Contact ID must be positive')
        return v
