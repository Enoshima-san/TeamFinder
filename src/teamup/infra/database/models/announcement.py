```python
from datetime import datetime
from uuid import uuid4

from sqlalchemy import UUID, Column, DateTime, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from .base import Base


class AnnouncementORM(Base):
    """
    ORM model for Announcement entity.
    """

    __tablename__ = "announcement"

    # Unique identifier for the announcement
    announcement_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)

    # Foreign key referencing the user who created the announcement
    user_id = Column(UUID(as_uuid=True), ForeignKey("user.user_id"), nullable=False)

    # Foreign key referencing the game associated with the announcement
    game_id = Column(UUID(as_uuid=True), ForeignKey("game.game_id"), nullable=True)

    # Type of announcement (e.g. "new game", "update", etc.)
    announcement_type = Column(String(100), nullable=True)

    # Minimum rank required to participate in the announcement
    rank_min = Column(Integer, nullable=True)

    # Maximum rank required to participate in the announcement
    rank_max = Column(Integer, nullable=True)

    # Description of the announcement
    description = Column(String(255), nullable=True)

    # Status of the announcement (e.g. "active", "inactive", etc.)
    status = Column(String(100), nullable=False, default="активный")

    # Timestamp when the announcement was created
    created_at = Column(DateTime, nullable=False, default=datetime.now)

    # Timestamp when the announcement was last updated
    updated_at = Column(
        DateTime, nullable=False, default=datetime.now, onupdate=datetime.now
    )

    # Relationship with the UserORM model
    user = relationship("UserORM", back_populates="announcements")

    # Relationship with the GameORM model
    game = relationship("GameORM", back_populates="announcements")

    # Relationship with the ResponseORM model
    responses = relationship("ResponseORM", back_populates="announcement")

    # Relationship with the ComplaintsORM model
    complaints = relationship("ComplaintsORM", back_populates="announcement")
```