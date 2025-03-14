from pydantic import BaseModel, EmailStr, Field
from typing import Optional
from datetime import date


'''Обычный пользователь'''
class EmailRequest(BaseModel):
    email: EmailStr = Field(..., max_length=50)

class UserCreate(BaseModel):
    first_name: Optional[str] = Field("", max_length=50)
    last_name: Optional[str] = Field("", max_length=50)
    uin: str = Field(..., min_length=12, max_length=12)  
    email: EmailStr = Field(..., max_length=50)
    phone_number: Optional[str] = Field(None, max_length=30)
    password: str = Field(..., min_length=8)  

class UserLogin(BaseModel):
    email: EmailStr = Field(..., max_length=50)
    password: str = Field(..., min_length=8)  

class VerifyEmail(BaseModel):
    code: str = Field(..., min_length=6, max_length=6)


'''Админ'''
class AdminLogin(BaseModel):
    username: str = Field(..., max_length=50)
    password: str = Field(..., min_length=4)

'''Создание полиций'''
class AdminCreatePolice(BaseModel):
    first_name: Optional[str] = Field("", max_length=50)
    last_name: Optional[str] = Field("", max_length=50)
    email: EmailStr = Field(..., max_length=50)
    phone_number: Optional[str] = Field(None, max_length=30)
    rank: Optional[str] = Field("", max_length=255)
    birth_day: Optional[date] 
    station_id: int

'''Полиция'''
class PoliceEmailRequest(BaseModel):
    email: EmailStr = Field(..., max_length=50)

class PoliceVerifyEmail(BaseModel):
    code: str = Field(..., min_length=6, max_length=6)