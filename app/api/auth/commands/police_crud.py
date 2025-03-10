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