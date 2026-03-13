from uuid import uuid4

from sqlalchemy import UUID, Boolean, Column, ForeignKey
from sqlalchemy.orm import relationship

from .base import Base


class UserGamesORM(Base):
    __tablename__ = "user_games"

    user_game_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    game_id = Column(UUID(as_uuid=True), ForeignKey("game.game_id"), nullable=False)
    user_id = Column(UUID(as_uuid=True), ForeignKey("user.user_id"), nullable=False)
    preferred = Column(Boolean, nullable=False, default=False)

    user = relationship("UserORM", back_populates="user_games")
    game = relationship("GameORM", back_populates="user_games")
