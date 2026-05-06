from uuid import uuid4

from sqlalchemy import UUID, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import Base


class AnnouncementGamesORM(Base):
    __tablename__ = "announcement_games"

    announcement_game_id: Mapped[UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid4
    )
    game_id = mapped_column(
        UUID(as_uuid=True),
        ForeignKey(
            "game.game_id",
            ondelete="CASCADE",
        ),
        nullable=False,
    )
    announcement_id: Mapped[UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey(
            "announcement.announcement_id",
            ondelete="CASCADE",
        ),
        nullable=False,
    )

    announcement = relationship(
        "AnnouncementORM", back_populates="announcement_games_link"
    )
    game = relationship("GameORM", back_populates="announcement_games_link")
