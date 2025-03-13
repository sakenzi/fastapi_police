import logging
from app.api.users.schemas.response import UserResponse
from sqlalchemy import select
from model.model import User
from fastapi import HTTPException
from core.config import settings
from sqlalchemy.ext.asyncio import AsyncSession


logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

async def get_user_by_email(db: AsyncSession, email: str) -> User:
    stmt = select(User).filter(User.email == email)
    result = await db.execute(stmt)
    user = result.scalar_one_or_none()

    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    logger.info(f"Profile retrieved for user id: {email}")
    return user