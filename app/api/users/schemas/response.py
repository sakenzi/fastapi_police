from pydantic import BaseModel, Field, EmailStr
from typing import Optional 
from datetime import date


class UserResponse(BaseModel):
    first_name: Optional[str] = Field(..., max_length=50)
    last_name: Optional[str] = Field(..., max_length=50)
    uin: str = Field(..., min_length=12, max_length=12)  
    email: EmailStr = Field(..., max_length=50)
    phone_number: Optional[str] = Field(None, max_length=30)
    birth_day: Optional[date]
    gender: Optional[str] = Field(..., max_length=20)