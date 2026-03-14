from uuid import uuid4

from sqlalchemy import UUID, LargeBinary, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import Base


class GameORM(Base):
    __tablename__ = "game"

    game_id: Mapped[UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid4
    )
    game_name: Mapped[str] = mapped_column(String(100), nullable=False)
    game_icon: Mapped[bytes] = mapped_column(LargeBinary, nullable=False)

    user_games = relationship("UserGamesORM", back_populates="game")
    announcement = relationship("AnnouncementORM", back_populates="game")
    rank = relationship("RankORM", back_populates="game")
    player_rating = relationship("PlayerRatingORM")
