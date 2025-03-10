from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.api.auth.schemas.create import AdminCreatePolice, PoliceEmailRequest, PoliceVerifyEmail
from app.api.auth.schemas.response import TokenResponse
from app.api.auth.commands.police_crud import create_policeman, send_police_verification_email, verify_police_email
from database.db import get_db

router = APIRouter()

@router.post(
    '/police/register',
    summary="Create or update a policeman by admin"
)
async def register_policeman(policeman: AdminCreatePolice,db: AsyncSession = Depends(get_db)):
    return await create_policeman(policeman=policeman, db=db)

@router.post(
    '/police/send-verification',
    summary="Send verification code to policeman's email"
)
async def send_verification(email_request: PoliceEmailRequest,db: AsyncSession = Depends(get_db)):
    return await send_police_verification_email(email_request=email_request, db=db)

@router.post(
    '/police/verify',
    summary="Verify policeman's email and login",
    response_model=TokenResponse
)
async def verify_email(verify_data: PoliceVerifyEmail,db: AsyncSession = Depends(get_db)):
    return await verify_police_email(verify_data=verify_data, db=db)