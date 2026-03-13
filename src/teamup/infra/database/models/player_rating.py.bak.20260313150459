from datetime import datetime
from uuid import uuid4

from sqlalchemy import UUID, Column, DateTime, ForeignKey, Integer
from sqlalchemy.orm import relationship

from .base import Base


class PlayerRatingORM(Base):
    __tablename__ = "player_rating"

    rating_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    game_id = Column(UUID(as_uuid=True), ForeignKey("game.game_id"), nullable=False)
    user_id = Column(UUID(as_uuid=True), ForeignKey("user.user_id"), nullable=False)
    response_id = Column(
        UUID(as_uuid=True),
        ForeignKey("response.response_id"),
        nullable=False,
    )
    rating_value = Column(Integer, nullable=False, default=0)
    created_at = Column(DateTime, nullable=False, default=datetime.now)

    user = relationship("UserORM", back_populates="player_rating")
    game = relationship("GameORM", back_populates="player_rating")
    response = relationship("ResponseORM", back_populates="player_rating")
