from datetime import datetime
from uuid import uuid4

from sqlalchemy import UUID, DateTime, ForeignKey, Integer
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import Base


class PlayerRatingORM(Base):
    __tablename__ = "player_rating"

    rating_id: Mapped[UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid4
    )
    game_id: Mapped[UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("game.game_id"), nullable=False
    )
    user_id: Mapped[UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("user.user_id"), nullable=False
    )
    response_id: Mapped[UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("response.response_id"),
        nullable=False,
    )
    rating_value: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    created_at: Mapped[datetime] = mapped_column(
        DateTime, nullable=False, default=datetime.now
    )

    user = relationship("UserORM", back_populates="player_rating")
    game = relationship("GameORM", back_populates="player_rating")
    response = relationship("ResponseORM", back_populates="player_rating")
