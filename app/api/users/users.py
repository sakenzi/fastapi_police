from fastapi import APIRouter, Depends, Request
from sqlalchemy.ext.asyncio import AsyncSession
from .schemas.create import *
from .schemas.response import UserResponse
from .commands.users_crud import *
from database.db import get_db
from app.api.auth.commands.context import validate_access_token_by_id, get_access_token


router = APIRouter()

@router.get(
    '/profile',
    summary='Get current user profile',
    response_model=UserResponse
)
async def user_profile(request: Request, db: AsyncSession = Depends(get_db)):
    access_token = await get_access_token(request)
    email = await validate_access_token_by_id(access_token) 
    return await get_user_by_email(email=email, db=db)

@router.post(
    '/call',
    summary='Create session call',
    response_model=CallCreate
)
async def session_call(request: Request, call: CallCreate, db: AsyncSession = Depends(get_db)):
    access_token = await get_access_token(request)
    email = await validate_access_token_by_id(access_token)
    return await create_call(call=call, db=db) 

'''IP-телефония через asterisk, но работает только через внутренний сеть'''
@router.post("/call/{to_extension}", summary="Initiate a call to another extension")
async def make_call(to_extension: str, request: Request, db: AsyncSession = Depends(get_db)):
    access_token = await get_access_token(request)
    email = await validate_access_token_by_id(access_token)
    user = await get_user_by_email(email=email, db=db)
    from_extension = "1001"  
    result = await initiate_call(from_extension, to_extension)
    return result