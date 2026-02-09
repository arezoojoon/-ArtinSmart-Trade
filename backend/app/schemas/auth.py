from typing import Optional
from pydantic import BaseModel, EmailStr
from uuid import UUID
from datetime import datetime


class Token(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str

class TokenData(BaseModel):
    sub: Optional[str] = None
    email: Optional[str] = None
    role: Optional[str] = None
    tenant_id: Optional[str] = None
    user_id: Optional[str] = None

class UserBase(BaseModel):
    email: EmailStr
    full_name: Optional[str] = None
    role: str = "buyer"

class UserCreate(UserBase):
    password: str
    tenant_name: Optional[str] = None

class LoginRequest(BaseModel):
    email: EmailStr
    password: str

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class ForgotPasswordRequest(BaseModel):
    email: EmailStr

class ResetPasswordRequest(BaseModel):
    token: str
    new_password: str

class UserResponse(UserBase):
    id: UUID
    tenant_id: UUID
    is_active: bool

    class Config:
        from_attributes = True

class UserDetailResponse(UserResponse):
    created_at: Optional[datetime] = None

    class Config:
        from_attributes = True
