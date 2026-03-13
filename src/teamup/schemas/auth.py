```python
from datetime import datetime
from typing import Optional
from uuid import UUID

from pydantic import BaseModel, EmailStr, Field

from ..domain import UserRole


class TokenData(BaseModel):
    """Data contained within a token."""
    user_id: UUID
    username: str
    role: str


class TokenPair(BaseModel):
    """Pair of access and refresh tokens."""
    access_token: str
    refresh_token: str
    token_type: str = "Bearer"


class RegisterRequest(BaseModel):
    """Request to register a new user."""
    email: EmailStr
    username: str
    password: str


class LoginRequest(BaseModel):
    """Request to login a user."""
    login: str | EmailStr = Field(..., alias="login")
    password: str


class UserResponse(BaseModel):
    """User data returned in a response."""
    username: str
    email: EmailStr
    registration_date: datetime
    last_login: datetime = datetime.now()
    is_active: bool = True
    role: str = UserRole.USER.value
    age: Optional[int] = None
    about_me: Optional[str] = None


# Example usage:
# user_response = UserResponse(username="john_doe", email="john@example.com", registration_date=datetime(2022, 1, 1))
```

```python
# Improved code with consistent naming conventions and docstrings
from datetime import datetime
from typing import Optional
from uuid import UUID

from pydantic import BaseModel, EmailStr, Field

from ..domain import UserRole


class UserTokenData(BaseModel):
    """Data contained within a user token."""
    user_id: UUID
    username: str
    role: str


class AccessTokenPair(BaseModel):
    """Pair of access and refresh tokens."""
    access_token: str
    refresh_token: str
    token_type: str = "Bearer"


class UserRegistrationRequest(BaseModel):
    """Request to register a new user."""
    email: EmailStr
    username: str
    password: str


class UserLoginRequest(BaseModel):
    """Request to login a user."""
    login: str | EmailStr = Field(..., alias="login")
    password: str


class UserResponseModel(BaseModel):
    """User data returned in a response."""
    username: str
    email: EmailStr
    registration_date: datetime
    last_login: datetime = datetime.now()
    is_active: bool = True
    role: str = UserRole.USER.value
    age: Optional[int] = None
    about_me: Optional[str] = None


# Example usage:
# user_response = UserResponseModel(username="john_doe", email="john@example.com", registration_date=datetime(2022, 1, 1))
```