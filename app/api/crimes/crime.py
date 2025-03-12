from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.api.crimes.schemas.create import CrimeCreate
from app.api.crimes.commands.crime_crud import create_crimes, all_crimes
from database.db import get_db

router = APIRouter()

@router.post(
    "/crime/add",
    summary="Add a list of crimes to the database"
)
async def add_crimes(crimes: list[CrimeCreate],db: AsyncSession = Depends(get_db)):
    return await create_crimes(crimes=crimes, db=db)

@router.get(
    "/crime/all_crimes",
    summary="Get all crimes",
    response_model=list[CrimeCreate]
)
async def all_crime(db: AsyncSession = Depends(get_db)):
    return await all_crimes(db=db)