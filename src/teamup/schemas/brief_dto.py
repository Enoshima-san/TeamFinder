import base64
from typing import Optional
from uuid import UUID

from pydantic import BaseModel

from src.teamup.domain import Game, User


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
