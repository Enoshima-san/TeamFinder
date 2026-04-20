from datetime import datetime
from uuid import uuid4

from sqlalchemy import UUID, Boolean, DateTime, ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from ..base import Base


class NotificationORM(Base):
    __tablename__ = "notification"

    notification_id: Mapped[UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid4
    )
    user_id: Mapped[UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("user.user_id", ondelete="CASCADE")
    )
    announcement_id: Mapped[UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("announcement.announcement_id", ondelete="CASCADE"),
    )
    conversation_id: Mapped[UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("conversation.conversation_id", ondelete="CASCADE"),
    )
    content: Mapped[str] = mapped_column(String(100), nullable=False)
    timestamp: Mapped[datetime] = mapped_column(
        DateTime, nullable=False, default=datetime.now
    )
    is_read: Mapped[bool] = mapped_column(Boolean, default=False)

    user = relationship("UserORM", back_populates="notification")
    announcement = relationship("AnnouncementORM", back_populates="notification")
    conversation = relationship("ConversationORM", back_populates="notification")
