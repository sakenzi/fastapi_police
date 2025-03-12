from sqlalchemy.ext.asyncio import AsyncSession
from model.model import Crime
from app.api.crimes.schemas.create import CrimeCreate
from app.api.crimes.schemas.response import CrimeWithGeom
import logging
from sqlalchemy import select, text

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


async def all_crimes(db: AsyncSession, latitude: float, longitude: float, distance: float):
    query = text("""
        SELECT id, street, ST_AsText(geom) as geom,
               data, geoposition, period, stat, time_period, organ, year,
               crime_code, hard_code, city_code, ud, objectid, home_number, reg_code
        FROM crimes
        WHERE ST_DWithin(
            geom::geography,
            ST_SetSRID(ST_MakePoint(:longitude, :latitude), 4326)::geography,
            :distance
        )
    """)

    result = await db.execute(query, {"longitude": longitude, "latitude": latitude, "distance": distance})
    crimes = result.fetchall()

    crime_list = [
        CrimeWithGeom(
            id=row[0],
            street=row[1],
            geom=row[2],
            data=row[3],
            geoposition=row[4],
            period=row[5],
            stat=row[6],
            time_period=row[7],
            organ=row[8],
            year=row[9],
            crime_code=row[10],
            hard_code=row[11],
            city_code=row[12],
            ud=row[13],
            objectid=row[14],
            home_number=row[15],
            reg_code=row[16]
        )
        for row in crimes
    ]
    logger.info(f"Retrieved {len(crime_list)} crimes within {distance} meters from ({latitude}, {longitude})")
    return crime_list