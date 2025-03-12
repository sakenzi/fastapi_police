from sqlalchemy.ext.asyncio import AsyncSession
from model.model import Crime
from app.api.crimes.schemas.create import CrimeCreate
import logging
from sqlalchemy import select

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

async def create_crimes(crimes: list[CrimeCreate], db: AsyncSession):
    '''Добавление преступлений'''
    db_crimes = []
    for crime_data in crimes:
        db_crime = Crime(
            data=crime_data.data,
            street=crime_data.street,
            geoposition=crime_data.geoposition,
            period=crime_data.period,
            stat=crime_data.stat,
            time_period=crime_data.time_period,
            organ=crime_data.organ,
            year=crime_data.year,
            crime_code=crime_data.crime_code,
            hard_code=crime_data.hard_code,
            city_code=crime_data.city_code,
            ud=crime_data.ud,
            objectid=crime_data.objectid,
            home_number=crime_data.home_number,
            reg_code=crime_data.reg_code
        )
        db_crimes.append(db_crime)
    
    db.add_all(db_crimes)
    await db.commit()
    logger.info(f"Added {len(db_crimes)} crimes to the database")
    return {"message": f"Successfully added {len(db_crimes)} crimes"}


async def all_crimes(db: AsyncSession):
    '''Выводить преступности'''
    stmt = select(Crime).filter(Crime.hard_code > "2")
    result = await db.execute(stmt)
    crimes = result.scalars().all()

    crime_list = [
        CrimeCreate(
            data=crime.data,
            street=crime.street,
            geoposition=crime.geoposition,
            period=crime.period,
            stat=crime.stat,
            time_period=crime.time_period,
            organ=crime.organ,
            year=crime.year,
            crime_code=crime.crime_code,
            hard_code=crime.hard_code,
            city_code=crime.city_code,
            ud=crime.ud,
            objectid=crime.objectid,
            home_number=crime.home_number,
            reg_code=crime.reg_code
        )
        for crime in crimes
    ]

    logger.info(f"Retrieved {len(crime_list)} crimes with time_period > 1")
    return crime_list

