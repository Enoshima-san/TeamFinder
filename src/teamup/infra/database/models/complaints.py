from datetime import datetime
from typing import Optional
from uuid import uuid4

from sqlalchemy import UUID, DateTime, ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.teamup.domain import ComplaintStatus

from .base import Base


class ComplaintsORM(Base):
    __tablename__ = "complaints"

    complaint_id: Mapped[UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid4
    )
    user_id: Mapped[UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("user.user_id"), nullable=False
    )
    announcement_id: Mapped[UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("announcement.announcement_id"), nullable=False
    )
    response_id: Mapped[UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("response.response_id"), nullable=False
    )
    status: Mapped[str] = mapped_column(
        String(20), nullable=False, default=ComplaintStatus.OPEN.value
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime, nullable=False, default=datetime.now
    )
    resolved_at: Mapped[Optional[datetime]] = mapped_column(DateTime, nullable=True)

    user = relationship("UserORM", back_populates="complaints")
    response = relationship("ResponseORM", back_populates="complaints")
    announcement = relationship("AnnouncementORM", back_populates="complaints")
