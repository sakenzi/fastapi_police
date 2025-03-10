import logging
from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession
from app.api.auth.schemas.create import UserCreate
from app.api.auth.schemas.response import TokenResponse
from model.model import User
from .context import create_access_token, hash_password, verify_password
from fastapi import HTTPException
from datetime import datetime
from .send_email import generate_verification_code, send_verification_email

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

async def send_verification_code_request(email: str, db: AsyncSession):
    """Отправка кода верификации по email без регистрации"""
    stmt = await db.execute(
        select(User).filter(User.email == email)
    )
    user = stmt.scalar_one_or_none()

    verification_code = await generate_verification_code()
    
    if user:
        await db.execute(
            update(User)
            .where(User.email == email)
            .values(verification_code=verification_code)
        )
    else:
        new_user = User(
            email=email,
            verification_code=verification_code,
            is_active=False
        )
        db.add(new_user)
    
    await db.commit()
    await send_verification_email(email, verification_code)
    return {"message": "Verification code sent to your email"}

async def user_register(user: UserCreate, db: AsyncSession):
    """Регистрация с обновлением существующего пользователя, сохраняя is_active для верифицированных"""
    stmt = await db.execute(
        select(User).filter(User.email == user.email)
    )
    existing_user = stmt.scalar_one_or_none()

    try:
        birth_year = int(user.uin[:2])
        birth_month = int(user.uin[2:4])
        birth_day = int(user.uin[4:6])
        birth_year_full = 1900 + birth_year if birth_year >= 23 else 2000 + birth_year
        birth_date = datetime(birth_year_full, birth_month, birth_day)
    except (ValueError, IndexError):
        raise HTTPException(status_code=400, detail="Invalid UIN format for birth date")

    gender_digit = user.uin[6]
    if gender_digit in '135':
        gender = "male"
    elif gender_digit in '246':
        gender = "female"
    else:
        raise HTTPException(status_code=400, detail="Invalid gender digit in UIN")

    hashed_password = hash_password(user.password)
    
    if existing_user:
        is_active = existing_user.is_active  
        verification_code = None if is_active else await generate_verification_code()  
        
        await db.execute(
            update(User)
            .where(User.email == user.email)
            .values(
                first_name=user.first_name,
                last_name=user.last_name,
                uin=user.uin,
                phone_number=user.phone_number,
                password=hashed_password,
                birth_day=birth_date,
                gender=gender,
                is_active=is_active,  
                verification_code=verification_code  
            )
        )
        logger.info(f"Updated user with email: {user.email}, is_active remains: {is_active}")
    else:
        verification_code = await generate_verification_code()
        new_user = User(
            first_name=user.first_name,
            last_name=user.last_name,
            uin=user.uin,
            email=user.email,
            phone_number=user.phone_number,
            password=hashed_password,
            birth_day=birth_date,
            gender=gender,
            is_active=False,  
            verification_code=verification_code
        )
        db.add(new_user)
        logger.info(f"Created new user with email: {user.email}, requires verification")
    
    await db.commit()
    return {"message": "User registered successfully" + ("" if existing_user and is_active else ", please verify your email")}

async def user_login(email: str, password: str, db: AsyncSession):
    """Вход через email и password"""
    stmt = await db.execute(
        select(User).filter(User.email == email)
    )
    user = stmt.scalar_one_or_none()

    if not user or not verify_password(password, user.password):
        raise HTTPException(
            status_code=401,
            detail="Incorrect email or password"
        )
    
    if not user.is_active:
        raise HTTPException(
            status_code=400,
            detail="Please verify your email first"
        )
    
    access_token, expire_time = create_access_token(data={"sub": user.email})
    return TokenResponse(
        access_token=access_token,
        access_token_expire_time=expire_time
    )

async def verify_user_email(email: str, code: str, db: AsyncSession):
    """Верификация email по коду"""
    stmt = await db.execute(
        select(User).filter(User.email == email)
    )
    user = stmt.scalar_one_or_none()

    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    if user.verification_code != code:
        raise HTTPException(status_code=400, detail="Invalid verification code")
    
    await db.execute(
        update(User)
        .where(User.email == email)
        .values(
            is_active=True,
            verification_code=None
        )
    )
    await db.commit()
    return {"message": "Email verified successfully"}