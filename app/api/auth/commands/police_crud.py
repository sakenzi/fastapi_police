import logging
from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession
from app.api.auth.schemas.create import AdminCreatePolice, PoliceEmailRequest, PoliceVerifyEmail
from app.api.auth.schemas.response import TokenResponse
from model.model import Policeman
from .context import create_access_token
from fastapi import HTTPException
from jose import jwt, JWTError
from core.config import settings
from .send_email_police import generate_verification_code, send_verification_email

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

async def create_policeman(policeman: AdminCreatePolice, db: AsyncSession):
    stmt = await db.execute(select(Policeman).filter(Policeman.email == policeman.email))
    existing_policeman = stmt.scalar_one_or_none()

    verification_code = await generate_verification_code()
    
    if existing_policeman:
        await db.execute(
            update(Policeman)
            .where(Policeman.email == policeman.email)
            .values(
                first_name=policeman.first_name,
                last_name=policeman.last_name,
                phone_number=policeman.phone_number,
                rank=policeman.rank,
                birth_day=policeman.birth_day,
                station_id=policeman.station_id,
                is_active=False,
                verification_code=verification_code
            )
        )
        logger.info(f"Updated policeman with email: {policeman.email}")
    else:
        new_policeman = Policeman(
            first_name=policeman.first_name,
            last_name=policeman.last_name,
            email=policeman.email,
            phone_number=policeman.phone_number,
            rank=policeman.rank,
            birth_day=policeman.birth_day,
            station_id=policeman.station_id,
            is_active=False,
            verification_code=verification_code
        )
        db.add(new_policeman)
        logger.info(f"Created new policeman with email: {policeman.email}")

    await db.commit()
    await send_verification_email(policeman.email, verification_code)
    return {"message": "Policeman created successfully, verification code sent"}

async def send_police_verification_email(email_request: PoliceEmailRequest, db: AsyncSession):
    stmt = await db.execute(select(Policeman).filter(Policeman.email == email_request.email))
    policeman = stmt.scalar_one_or_none()

    if not policeman:
        raise HTTPException(status_code=404, detail="Policeman not found")
    
    verification_code = await generate_verification_code()
    await db.execute(
        update(Policeman)
        .where(Policeman.email == email_request.email)
        .values(verification_code=verification_code)
    )
    await db.commit()

    access_token, expire_time = create_access_token(data={"sub": email_request.email})
    
    await send_verification_email(email_request.email, verification_code)
    
    return TokenResponse(
        access_token=access_token,
        access_token_expire_time=expire_time,
        message="Verification code sent to your email"
    )

async def verify_police_email(token: str, code: str, db: AsyncSession):
    try:
        payload = jwt.decode(token, settings.TOKEN_SECRET_KEY, algorithms=[settings.TOKEN_ALGORITHM])
        email: str = payload.get("sub")
        if email is None:
            raise HTTPException(status_code=401, detail="Invalid token: email not found")
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid or expired token")

    stmt = await db.execute(select(Policeman).filter(Policeman.email == email))
    policeman = stmt.scalar_one_or_none()

    if not policeman:
        raise HTTPException(status_code=404, detail="Policeman not found")
    
    if policeman.verification_code != code:
        raise HTTPException(status_code=400, detail="Invalid verification code")
    
    await db.execute(
        update(Policeman)
        .where(Policeman.email == email)
        .values(
            is_active=True,
            verification_code=None
        )
    )
    await db.commit()

    access_token, expire_time = create_access_token(data={"sub": policeman.email})
    return TokenResponse(
        access_token=access_token,
        access_token_expire_time=expire_time,
        message="Email verified successfully"
    )