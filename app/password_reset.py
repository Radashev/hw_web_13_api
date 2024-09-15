from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from app.db import get_db

router = APIRouter()


@router.post("/password_reset/")
async def request_password_reset(email: str, db: AsyncSession = Depends(get_db)):
    # Логіка для запиту скидання пароля
    return {"message": "Password reset requested"}
