from datetime import datetime
from uuid import uuid4

from sqlalchemy import UUID, Column, DateTime, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from .base import Base


class AnnouncementORM(Base):
    __tablename__ = "announcement"

    announcement_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("user.user_id"), nullable=False)
    game_id = Column(UUID(as_uuid=True), ForeignKey("game.game_id"), nullable=True)
    type = Column(String(100), nullable=True)
    rank_min = Column(Integer, nullable=True)
    rank_max = Column(Integer, nullable=True)
    description = Column(String(255), nullable=True)
    status = Column(String(100), nullable=False, default="активный")
    created_at = Column(DateTime, nullable=False, default=datetime.now)
    updated_at = Column(
        DateTime, nullable=False, default=datetime.now, onupdate=datetime.now
    )

    user = relationship("UserORM", back_populates="announcement")
    game = relationship("GameORM", back_populates="announcement")
    response = relationship("ResponseORM", back_populates="announcement")
    complaints = relationship("ComplaintsORM", back_populates="announcement")
