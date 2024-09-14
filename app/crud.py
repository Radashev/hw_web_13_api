from sqlalchemy.orm import Session
from sqlalchemy import or_, and_
from datetime import date, timedelta
# from . import models, schemas
from app import models, schemas


def get_user_by_email(db: Session, email: str):
    return db.query(models.User).filter(models.User.email == email).first()


def get_contact(db: Session, contact_id: int, user_id: int):
    return db.query(models.Contact).filter(and_(models.Contact.id == contact_id, models.Contact.owner_id == user_id)).first()


def get_contacts(
        db: Session,
        skip: int = 0,
        limit: int = 10,
        name: str = None,
        last_name: str = None,
        email: str = None,
        user_id: int = None
):
    query = db.query(models.Contact).filter(models.Contact.owner_id == user_id)
    if name:
        query = query.filter(models.Contact.first_name.ilike(f"%{name}%"))
    if last_name:
        query = query.filter(models.Contact.last_name.ilike(f"%{last_name}%"))
    if email:
        query = query.filter(models.Contact.email.ilike(f"%{email}%"))
    return query.offset(skip).limit(limit).all()


def create_contact(db: Session, contact: schemas.ContactCreate, user_id: int):
    db_contact = models.Contact(**contact.dict(), owner_id=user_id)
    db.add(db_contact)
    db.commit()
    db.refresh(db_contact)
    return db_contact


def update_contact(db: Session, contact_id: int, contact: schemas.ContactUpdate, user_id: int):
    db_contact = db.query(models.Contact).filter(and_(models.Contact.id == contact_id, models.Contact.owner_id == user_id)).first()
    if db_contact:
        for key, value in contact.dict().items():
            setattr(db_contact, key, value)
        db.commit()
        db.refresh(db_contact)
    return db_contact


def delete_contact(db: Session, contact_id: int, user_id: int):
    db_contact = db.query(models.Contact).filter(and_(models.Contact.id == contact_id, models.Contact.owner_id == user_id)).first()
    if db_contact:
        db.delete(db_contact)
        db.commit()
    return db_contact


def get_contacts_with_upcoming_birthdays(db: Session, user_id: int, days: int = 7):
    today = date.today()
    end_date = today + timedelta(days=days)
    return db.query(models.Contact).filter(
        and_(
            models.Contact.owner_id == user_id,
            models.Contact.birth_date >= today,
            models.Contact.birth_date <= end_date
        )
    ).all()
