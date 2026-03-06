from uuid import uuid4

from sqlalchemy import UUID, Column, LargeBinary, String
from sqlalchemy.orm import relationship

from .base import Base


class Game(Base):
    __tablename__ = "game"

    game_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    game_name = Column(String(100), nullable=False)
    game_icon = Column(LargeBinary, nullable=False)

    user_games = relationship("UserGames", back_populates="game")
    announcements = relationship("Announcement", back_populates="game")
    ranks = relationship("Rank", back_populates="game")
