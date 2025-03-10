from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.api.auth.schemas.response import TokenResponse
from model.model import Admin
from .context import create_access_token, verify_password
from fastapi import HTTPException


async def admin_login(username: str, password: str, db: AsyncSession):
    stmt = await db.execute(
        select(Admin).filter(Admin.username == username)
    )
    admin = stmt.scalar_one_or_none()

    if not admin or not verify_password(password, admin.password):
        raise HTTPException(
            status_code=401,
            detail="Incorrect password"
        )
    
    access_token, expire_time = create_access_token(data={"sub": admin.username})
    return TokenResponse(
        access_token=access_token,
        access_token_expire_time=expire_time
    )