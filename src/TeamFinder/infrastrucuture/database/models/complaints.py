from datetime import datetime
from uuid import uuid4

from sqlalchemy import UUID, Column, DateTime, ForeignKey, Integer, String

from ....domain.enums import ComplaintStatus
from .base import Base


class ComplaintsORM(Base):
    __tablename__ = "complaints"

    complaint_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    user_id = Column(Integer, ForeignKey("user.user_id"), nullable=False)
    announcement_id = Column(
        Integer, ForeignKey("announcement.announcement_id"), nullable=False
    )
    response_id = Column(Integer, ForeignKey("response.response_id"), nullable=False)
    status = Column(String(20), nullable=False, default=ComplaintStatus.OPEN.value)
    created_at = Column(DateTime, nullable=False, default=datetime.now)
    resolved_at = Column(DateTime, nullable=True)
