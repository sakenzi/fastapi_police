from pydantic import BaseModel, Field
from typing import Optional

class CrimeWithGeom(BaseModel):
    id: int
    street: Optional[str] = Field("", max_length=255)
    geom: Optional[str] = Field(None)  
    data: Optional[str] = Field("", max_length=255)
    geoposition: Optional[str] = Field("", max_length=255)
    period: Optional[str] = Field("", max_length=255)
    stat: Optional[str] = Field("", max_length=255)
    time_period: Optional[int] = Field(0)
    organ: Optional[str] = Field("", max_length=255)
    year: Optional[str] = Field("", max_length=255)
    crime_code: Optional[str] = Field("", max_length=255)
    hard_code: Optional[str] = Field("", max_length=255)
    city_code: Optional[str] = Field("", max_length=255)
    ud: Optional[str] = Field("", max_length=255)
    objectid: Optional[str] = Field("", max_length=255)
    home_number: Optional[str] = Field("", max_length=255)
    reg_code: Optional[str] = Field("", max_length=255)

    class Config:
        from_attributes = True