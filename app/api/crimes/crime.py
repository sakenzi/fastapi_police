from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.api.crimes.schemas.create import CrimeCreate
from app.api.crimes.commands.crime_crud import create_crimes
from database.db import get_db

router = APIRouter()

@router.post(
    "/add",
    summary="Add a list of crimes to the database"
)
async def add_crimes(
    crimes: list[CrimeCreate],
    db: AsyncSession = Depends(get_db)
):
    return await create_crimes(crimes=crimes, db=db)