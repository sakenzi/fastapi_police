import logging
from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession
from app.api.auth.schemas.create import AdminCreatePolice, PoliceEmailRequest, PoliceVerifyEmail, PoliceLogin
from app.api.auth.schemas.response import TokenResponse
from model.model import Policeman
from .context import create_access_token, hash_password, verify_password
from fastapi import HTTPException
from datetime import datetime
from .send_email import generate_verification_code, send_verification_email


logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

async def create_policeman(policeman: AdminCreatePolice, db: AsyncSession):
    stmt = await db.execute(select(Policeman).filter(Policeman.email == policeman.email))

    existing_policeman = stmt.scalar_one_or_none()

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
                verification_code=await generate_verification_code()
            )
        )
        logger.info(f"Updated policeman with email: {policeman.email}")
    else:
        verification_code = await generate_verification_code()
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

    await send_verification_email(email_request.email, verification_code)
    return {"message": "Verification code sent to your email"}

async def verify_police_email(verify_data: PoliceVerifyEmail, db: AsyncSession):
    stmt = await db.execute(select(Policeman).filter(Policeman.email == verify_data.email))

    policeman = stmt.scalar_one_or_none()

    if not policeman:
        raise HTTPException(status_code=404, detail="Policeman not found")
    
    if policeman.verification_code != verify_data.code:
        raise HTTPException(status_code=400, detail="Invalid verification code")
    
    await db.execute(
        update(Policeman)
        .where(Policeman.email == verify_data.email)
        .values(
            is_active=True,
            verification_code=None
        )
    )
    await db.commit()

    access_token, expire_time = create_access_token(data={"sub": policeman.email})
    return TokenResponse(
        access_token=access_token,
        access_token_expire_time=expire_time
    )