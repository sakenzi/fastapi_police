from pydantic import BaseModel, Field
from typing import Optional

class CrimeWithGeom(BaseModel):
    id: int
    geom: Optional[str] = Field(None)  
    geoposition: Optional[str] = Field("", max_length=255)
    stat: Optional[str] = Field("", max_length=255)
    hard_code: Optional[str] = Field("", max_length=255)

    class Config:
        from_attributes = True