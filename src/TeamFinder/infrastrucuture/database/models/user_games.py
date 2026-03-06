from uuid import uuid4

from sqlalchemy import UUID, Boolean, Column, ForeignKey

from .base import Base


class UserGames(Base):
    __tablename__ = "user_games"

    user_game_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    game_id = Column(UUID(as_uuid=True), ForeignKey("game.game_id"), nullable=False)
    user_id = Column(UUID(as_uuid=True), ForeignKey("user.user_id"), nullable=False)
    preffered = Column(Boolean, nullable=False, default=False)
