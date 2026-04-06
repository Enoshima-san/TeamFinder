from datetime import datetime
from typing import Optional
from uuid import UUID

from pydantic import BaseModel

from teamup.domain import Announcement, Game, User

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

    def update_entity(self, announcement: Announcement) -> Announcement:
        announcement.type = self.type
        announcement.description = self.description
        announcement.rank_min = self.rank_min
        announcement.rank_max = self.rank_max
        announcement.status = self.status
        return announcement


class AnnouncementSummaryOut(BaseModel):
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
    def create(
        announcement: Announcement, user: User, game: Game
    ) -> "AnnouncementSummaryOut":
        return AnnouncementSummaryOut(
            announcement_id=announcement.announcement_id,
            type=announcement.type,
            description=announcement.description,
            rank_min=announcement.rank_min,
            rank_max=announcement.rank_max,
            status=announcement.status,
            updated_at=announcement.updated_at,
            user=UserBriefDto.from_user(user),
            game=GameBriefDto.from_game(game),
        )

    def update(self, u_ann: "AnnouncementUpdateIn"):
        self.type = u_ann.type
        self.description = u_ann.description
        self.rank_min = u_ann.rank_min
        self.rank_max = u_ann.rank_max
        self.status = u_ann.status
        self.updated_at = datetime.now()
