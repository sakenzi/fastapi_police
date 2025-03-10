from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from .schemas.create import *
from .schemas.response import TokenResponse
from .commands.auth_crud import *
from database.db import get_db


router  = APIRouter()

@router.post(
    '/send_email',
    summary="Send verification code to email"
)
async def send_verification(email_request: EmailRequest, db: AsyncSession = Depends(get_db)):
    return await send_verification_code_request(email_request.email, db)

@router.post(
    '/register',
    summary="Register a new user"
)
async def register(user: UserCreate, db: AsyncSession = Depends(get_db)):
    return await user_register(user=user, db=db)

@router.post(
    '/login',
    summary="Login user",
    response_model=TokenResponse
)
async def login(login_data: UserLogin, db: AsyncSession = Depends(get_db)):
    return await user_login(email=login_data.email, password=login_data.password, db=db)

@router.post(
    '/verify',
    summary="Verify email address with code"
)
async def verify(verification: VerifyEmail, db: AsyncSession = Depends(get_db)):
    return await verify_user_email(email=verification.email, code=verification.code, db=db)
