from datetime import datetime
from typing import Optional
from uuid import UUID

from pydantic import BaseModel

from .brief_dto import AnnouncementBriefDto, GameBriefDto, ResponseBriefDto


class FullUserInfoResponse(BaseModel):
    user_id: UUID
    email: str
    username: str
    registration_date: datetime
    last_login: datetime
    is_active: bool
    role: str
    has_microphone: bool
    age: int | None
    about_me: str | None
    is_blocked: bool
    blocked_reason: str | None

    games: list[GameBriefDto]
    announcements: list[AnnouncementBriefDto]
    responses: list[ResponseBriefDto]


class UserUpdateRequest(BaseModel):
    user_id: UUID
    username: Optional[str] = None
    about_me: Optional[str] = None


class UserUpdateResponse(BaseModel):
    user_id: UUID
    username: str
    about_me: Optional[str]
