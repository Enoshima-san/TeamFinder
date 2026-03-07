from datetime import datetime
from uuid import uuid4

from sqlalchemy import UUID, Column, DateTime, ForeignKey, Integer

from .base import Base


class PlayerRatingORM(Base):
    __tablename__ = "player_raiting"

    reiting_id = Column(UUID(as_uuid=True), primary_key=True, defualt=uuid4)
    game_id = Column(UUID(as_uuid=True), ForeignKey("game.game_id"), nullable=False)
    user_id = Column(UUID(as_uuid=True), ForeignKey("user.user_id"), nullable=False)
    reponse_id = Column(
        UUID(as_uuid=True),
        ForeignKey("response.reponse_id"),
        nullable=False,
    )
    raiting_value = Column(Integer, nullable=False, default=0)
    created_at = Column(DateTime, nullable=False, default=datetime.now)
