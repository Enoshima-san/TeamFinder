from datetime import datetime
from uuid import uuid4

from sqlalchemy import UUID, DateTime, ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.teamup.domain import ResponseStatus

from .base import Base


class ResponseORM(Base):
    __tablename__ = "response"

    response_id: Mapped[UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid4
    )
    announcement_id: Mapped[UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("announcement.announcement_id"), nullable=False
    )
    user_id: Mapped[UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("user.user_id"), nullable=False
    )
    status: Mapped[str] = mapped_column(
        String(20), nullable=False, default=ResponseStatus.PENDING.value
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime, nullable=False, default=datetime.now
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime, nullable=False, default=datetime.now, onupdate=datetime.now
    )
    announcement = relationship("AnnouncementORM", back_populates="response")
    complaints = relationship("ComplaintsORM", back_populates="response")
    user = relationship("UserORM", back_populates="response")
    player_rating = relationship("PlayerRatingORM", back_populates="response")
