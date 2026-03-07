from uuid import uuid4

from sqlalchemy import UUID, Column, LargeBinary, String
from sqlalchemy.orm import relationship

from .base import Base


class GameORM(Base):
    __tablename__ = "game"

    game_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    game_name = Column(String(100), nullable=False)
    game_icon = Column(LargeBinary, nullable=False)

    user_games = relationship("UserGamesORM", back_populates="game")
    announcements = relationship("AnnouncementORM", back_populates="game")
    ranks = relationship("RankORM", back_populates="game")
