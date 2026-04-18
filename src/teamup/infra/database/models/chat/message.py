from datetime import datetime
from typing import Optional
from uuid import uuid4

from sqlalchemy import UUID, Boolean, DateTime, ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from ..base import Base


class MessageORM(Base):
    __tablename__ = "message"

    message_id: Mapped[UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid4
    )
    sender_id: Mapped[UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("user.user_id", ondelete="CASCADE"),
        nullable=False,
    )
    recipient_id: Mapped[UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("user.user_id", ondelete="CASCADE"),
        nullable=False,
    )
    conversation_id: Mapped[UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("conversation.conversation_id", ondelete="CASCADE"),
        nullable=False,
    )

    content: Mapped[str] = mapped_column(String(255), nullable=False)
    created_at: Mapped[datetime] = mapped_column(
        DateTime, nullable=False, default=datetime.now
    )
    edited_at: Mapped[Optional[datetime]] = mapped_column(DateTime, nullable=True)
    is_deleted: Mapped[bool] = mapped_column(Boolean, default=False)
    deleted_at: Mapped[Optional[datetime]] = mapped_column(DateTime, nullable=True)
    is_read: Mapped[bool] = mapped_column(Boolean, default=False)
    read_at: Mapped[Optional[datetime]] = mapped_column(DateTime, nullable=True)
    conversation = relationship("ConversationORM", back_populates="messages")
    sender = relationship("UserORM", foreign_keys=[sender_id])
    recipient = relationship("UserORM", foreign_keys=[recipient_id])
