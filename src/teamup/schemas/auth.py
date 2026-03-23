from datetime import datetime
from typing import Optional
from uuid import UUID

from pydantic import BaseModel, EmailStr, Field

from ..domain import UserRole


class JwtPayload(BaseModel):
    sub: str
    username: str
    role: UserRole
    exp: int


class TokenData(BaseModel):
    user_id: UUID
    username: str
    role: UserRole
    exp: int


class TokenPair(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "Bearer"


class RegisterRequest(BaseModel):
    email: EmailStr
    username: str = Field(
        ...,
        min_length=3,
        max_length=15,
        pattern=r"^[a-z0-9_]+$",
        description="Только маленькие буквы, цифры и подчеркивание. Без пробелов.",
    )
    password: str = Field(..., min_length=8)


class LoginRequest(BaseModel):
    login: str = Field(..., max_length=50, description="Email или имя пользователя")
    password: str = Field(..., min_length=1)


class UserResponse(BaseModel):
    username: str
    email: EmailStr
    registration_date: datetime
    last_login: datetime = datetime.now()
    is_active: bool = True
    role: str = UserRole.USER.value
    age: Optional[int] = None
    about_me: Optional[str] = None
