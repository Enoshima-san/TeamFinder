from uuid import uuid4

from sqlalchemy import UUID, Column, ForeignKey, Integer, String

from .base import Base


class Rank(Base):
    __tablename__ = "rank"

    rank_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    game_id = Column(UUID(as_uuid=True), ForeignKey("game.game_id"), nullable=False)
    rank_level = Column(Integer, nullable=False, default=0)
    rank_name = Column(String(100), nullable=False)
