from datetime import datetime
from uuid import uuid4

from sqlalchemy import UUID, Column, DateTime, ForeignKey, String
from sqlalchemy.orm import relationship

from src.teamup.domain import ComplaintStatus

from .base import Base


class ComplaintsORM(Base):
    __tablename__ = "complaints"

    complaint_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("user.user_id"), nullable=False)
    announcement_id = Column(
        UUID(as_uuid=True), ForeignKey("announcement.announcement_id"), nullable=False
    )
    response_id = Column(
        UUID(as_uuid=True), ForeignKey("response.response_id"), nullable=False
    )
    status = Column(String(20), nullable=False, default=ComplaintStatus.OPEN.value)
    created_at = Column(DateTime, nullable=False, default=datetime.now)
    resolved_at = Column(DateTime, nullable=True)

    user = relationship("UserORM", back_populates="complaints")
    response = relationship("ResponseORM", back_populates="complaints")
    announcement = relationship("AnnouncementORM", back_populates="complaints")
