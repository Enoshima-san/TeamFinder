from datetime import datetime
from typing import Optional
from uuid import UUID

from pydantic import BaseModel

from src.teamup.domain import Announcement, Game, User

from .brief_dto import GameBriefDto, UserBriefDto


class AnnouncementCreateIn(BaseModel):
    type: str
    game_id: UUID
    description: Optional[str] = None
    rank_min: Optional[int] = None
    rank_max: Optional[int] = None

    def check_rank_range(self) -> bool:
        if (self.rank_min is not None) and (self.rank_max is not None):
            if self.rank_min > self.rank_max:
                return False
        return True


class AnnouncementUpdateIn(BaseModel):
    announcement_id: UUID
    type: str
    description: Optional[str]
    rank_min: Optional[int]
    rank_max: Optional[int]
    status: str
    updated_at: datetime


class AnnouncementOut(BaseModel):
    announcement_id: UUID
    type: str
    description: Optional[str]
    rank_min: Optional[int]
    rank_max: Optional[int]
    status: str
    updated_at: datetime

    user: UserBriefDto
    game: GameBriefDto

    @staticmethod
    def create(model: Announcement, user: User, game: Game) -> "AnnouncementOut":
        return AnnouncementOut(
            announcement_id=model.announcement_id,
            type=model.type,
            description=model.description,
            rank_min=model.rank_min,
            rank_max=model.rank_max,
            status=model.status,
            updated_at=model.updated_at,
            user=UserBriefDto.from_user(user),
            game=GameBriefDto.from_game(game),
        )


class AnnouncementSummaryOut(BaseModel):
    announcement_id: UUID
    type: str
    rank_min: Optional[int]
    rank_max: Optional[int]
    status: str

    user: UserBriefDto
    game: GameBriefDto
