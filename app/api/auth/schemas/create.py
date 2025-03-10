from pydantic import BaseModel, EmailStr, Field
from typing import Optional
from datetime import datetime


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
    email: EmailStr = Field(..., max_length=50)
    code: str = Field(..., min_length=6, max_length=6)


'''Админ'''
class AdminLogin(BaseModel):
    username: str = Field(..., max_length=50)
    password: str = Field(..., min_length=4)


'''Полиция'''
class PoliceEmailRequest(BaseModel):
    email: EmailStr = Field(..., max_length=50)

class PoliceVerifyEmail(BaseModel):
    email: EmailStr = Field(..., max_length=50)
    code: str = Field(..., min_length=6, max_length=6) 