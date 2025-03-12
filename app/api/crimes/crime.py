from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession
from app.api.crimes.schemas.create import CrimeCreate
from app.api.crimes.schemas.response import CrimeWithGeom
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
    summary="Get crimes within a specified distance from a point",
    response_model=list[CrimeWithGeom]
)
async def get_crimes_near_point(
    latitude: float = Query(..., description="Latitude of the point"),
    longitude: float = Query(..., description="Longitude of the point"),
    distance: float = Query(..., description="Distance in meters"),
    db: AsyncSession = Depends(get_db)
):
    return await all_crimes(db=db, latitude=latitude, longitude=longitude, distance=distance)