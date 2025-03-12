from pydantic import BaseModel, Field
from typing import Optional

class CrimeCreate(BaseModel):
    data: Optional[str] = Field("", max_length=255)  
    street: Optional[str] = Field("", max_length=255)
    geom: Optional[str] = Field(None)
    geoposition: Optional[str] = Field("", max_length=255)
    period: Optional[str] = Field("", max_length=255)
    stat: Optional[str] = Field("", max_length=255)
    time_period: Optional[str] = Field("", max_length=255)
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
        allow_population_by_field_name = True

        fields = {
            "data": {"alias": "dat_sover"},
            "year": {"alias": "yr"}
        }