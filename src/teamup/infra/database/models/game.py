from uuid import uuid4

from sqlalchemy import UUID, LargeBinary, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .announcement import AnnouncementORM
from .announcement_games import AnnouncementGamesORM
from .base import Base


class GameORM(Base):
    __tablename__ = "game"

    game_id: Mapped[UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid4
    )
    game_name: Mapped[str] = mapped_column(String(100), nullable=False)
    game_icon: Mapped[bytes] = mapped_column(LargeBinary, nullable=False)

    user_games = relationship(
        "UserGamesORM",
        back_populates="game",
        cascade="all, delete-orphan",
        passive_deletes=True,
    )
    announcements: Mapped[list["AnnouncementORM"]] = relationship(
        "AnnouncementORM",
        secondary=AnnouncementGamesORM.__table__,
        back_populates="games",
    )
    announcement_games_link = relationship(
        "AnnouncementGamesORM", back_populates="game"
    )
    rank = relationship(
        "RankORM",
        back_populates="game",
        cascade="all, delete-orphan",
        passive_deletes=True,
    )
    player_rating = relationship(
        "PlayerRatingORM",
        cascade="all, delete-orphan",
        passive_deletes=True,
    )
