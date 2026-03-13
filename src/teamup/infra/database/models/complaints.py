```python
from datetime import datetime
from uuid import uuid4

from sqlalchemy import Column, DateTime, ForeignKey, String, UUID
from sqlalchemy.orm import relationship

from src.teamup.domain import ComplaintStatus
from src.teamup.orm.base import Base  # Assuming the base class is in a different module


class ComplaintORM(Base):
    """
    SQLAlchemy ORM representation of a complaint.
    """

    __tablename__ = "complaints"

    # Unique identifier for the complaint
    complaint_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)

    # Foreign key referencing the user who submitted the complaint
    user_id = Column(UUID(as_uuid=True), ForeignKey("user.user_id"), nullable=False)

    # Foreign key referencing the announcement related to the complaint
    announcement_id = Column(
        UUID(as_uuid=True), ForeignKey("announcement.announcement_id"), nullable=False
    )

    # Foreign key referencing the response related to the complaint
    response_id = Column(
        UUID(as_uuid=True), ForeignKey("response.response_id"), nullable=False
    )

    # Status of the complaint (e.g., open, resolved, etc.)
    status = Column(String(20), nullable=False, default=ComplaintStatus.OPEN.value)

    # Timestamp when the complaint was created
    created_at = Column(DateTime, nullable=False, default=datetime.utcnow)

    # Timestamp when the complaint was resolved (if applicable)
    resolved_at = Column(DateTime, nullable=True)

    # Relationship with the user who submitted the complaint
    user = relationship("UserORM", back_populates="complaints")

    # Relationship with the response related to the complaint
    response = relationship("ResponseORM", back_populates="complaints")

    # Relationship with the announcement related to the complaint
    announcement = relationship("AnnouncementORM", back_populates="complaints")
```