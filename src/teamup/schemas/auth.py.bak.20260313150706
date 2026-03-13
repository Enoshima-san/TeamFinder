from datetime import datetime
from typing import Optional
from uuid import UUID

from pydantic import BaseModel, EmailStr, Field

from ..domain import UserRole


class TokenData(BaseModel):
    user_id: UUID
    username: str
    role: str


class TokenPair(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "Bearer"


class RegisterRequest(BaseModel):
    email: EmailStr
    username: str
    password: str


class LoginRequest(BaseModel):
    login: str | EmailStr = Field(..., alias="login")
    password: str


class UserResponse(BaseModel):
    username: str
    email: EmailStr
    registration_date: datetime
    last_login: datetime = datetime.now()
    is_active: bool = True
    role: str = UserRole.USER.value
    age: Optional[int] = None
    about_me: Optional[str] = None
