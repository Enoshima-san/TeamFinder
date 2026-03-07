from datetime import datetime
from uuid import uuid4

from sqlalchemy import UUID, Column, DateTime, ForeignKey, String
from sqlalchemy.orm import relationship

from ....domain.enums import ResponseStatus
from .base import Base


class ResponseORM(Base):
    __tablename__ = "response"

    response_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    announcement_id = Column(
        UUID(as_uuid=True), ForeignKey("announcement.announcement_id"), nullable=False
    )
    user_id = Column(UUID(as_uuid=True), ForeignKey("user.user_id"), nullable=False)
    status = Column(String(20), nullable=False, default=ResponseStatus.PENDING.value)
    created_at = Column(DateTime, nullable=False, default=datetime.now)
    updated_at = Column(
        DateTime, nullable=False, default=datetime.now, onupdate=datetime.now
    )

    complaints = relationship("ComplaintsORM", back_populates="response")
