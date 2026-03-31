import base64
from datetime import datetime
from typing import Optional
from uuid import UUID

from pydantic import BaseModel

from teamup.domain import Announcement, Game, Response, User


class UserBriefDto(BaseModel):
    user_id: UUID
    username: str
    has_microphone: bool
    age: Optional[int]
    about_me: Optional[str]
    is_blocked: bool
    blocked_reason: Optional[str]

    @staticmethod
    def from_user(user: User):
        return UserBriefDto(
            user_id=user.user_id,
            username=user.username,
            has_microphone=user.has_microphone,
            age=user.age,
            about_me=user.about_me,
            is_blocked=user.is_blocked,
            blocked_reason=user.blocked_reason,
        )


class GameBriefDto(BaseModel):
    game_id: UUID
    game_name: str
    game_icon: str

    @staticmethod
    def from_game(game: Game):
        return GameBriefDto(
            game_id=game.game_id,
            game_name=game.game_name,
            game_icon=base64.b64encode(game.game_icon).decode("utf-8"),
        )


class AnnouncementBriefDto(BaseModel):
    announcement_id: UUID
    type: str
    rank_min: int | None
    rank_max: int | None
    description: str | None
    status: str
    created_at: datetime
    updated_at: datetime

    @staticmethod
    def from_announcement(announcement: Announcement):
        return AnnouncementBriefDto(
            announcement_id=announcement.announcement_id,
            type=announcement.type,
            rank_min=announcement.rank_min,
            rank_max=announcement.rank_max,
            description=announcement.description,
            status=announcement.status,
            created_at=announcement.created_at,
            updated_at=announcement.updated_at,
        )


class ResponseBriefDto(BaseModel):
    response_id: UUID
    status: str
    created_at: datetime
    updated_at: datetime

    @staticmethod
    def from_response(response: Response):
        return ResponseBriefDto(
            response_id=response.response_id,
            status=response.status,
            created_at=response.created_at,
            updated_at=response.updated_at,
        )
