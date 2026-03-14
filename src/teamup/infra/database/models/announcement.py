from datetime import datetime
from typing import Optional
from uuid import uuid4

from sqlalchemy import UUID, DateTime, ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import Base


class AnnouncementORM(Base):
    __tablename__ = "announcement"

    announcement_id: Mapped[UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid4
    )
    user_id: Mapped[UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("user.user_id"), nullable=False
    )
    game_id: Mapped[Optional[UUID]] = mapped_column(
        UUID(as_uuid=True), ForeignKey("game.game_id"), nullable=True
    )
    type: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)
    rank_min: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    rank_max: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    description: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    status: Mapped[str] = mapped_column(String(100), nullable=False, default="активный")
    created_at: Mapped[datetime] = mapped_column(
        DateTime, nullable=False, default=datetime.now
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime, nullable=False, default=datetime.now, onupdate=datetime.now
    )

    user = relationship("UserORM", back_populates="announcement")
    game = relationship("GameORM", back_populates="announcement")
    response = relationship("ResponseORM", back_populates="announcement")
    complaints = relationship("ComplaintsORM", back_populates="announcement")
