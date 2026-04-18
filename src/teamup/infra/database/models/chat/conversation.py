from datetime import datetime
from typing import Optional
from uuid import uuid4

from sqlalchemy import UUID, DateTime, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from ..base import Base


class ConversationORM(Base):
    __tablename__ = "conversation"
    conversation_id: Mapped[UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid4
    )

    announcement_id: Mapped[UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("announcement.announcement_id", ondelete="CASCADE"),
        nullable=False,
    )
    announcement_author_id: Mapped[UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("user.user_id", ondelete="CASCADE"),
        nullable=False,
    )
    responder_id: Mapped[UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("user.user_id", ondelete="CASCADE"),
        nullable=False,
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime, nullable=False, default=datetime.now
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime, nullable=False, default=datetime.now, onupdate=datetime.now
    )
    last_message_at: Mapped[Optional[datetime]] = mapped_column(DateTime, nullable=True)
    messages = relationship(
        "MessageORM",
        back_populates="conversation",
        cascade="all, delete-orphan",
        passive_deletes=True,
    )
    author = relationship(
        "UserORM",
        foreign_keys=[announcement_author_id],
        back_populates="authored_conversations",
    )
    responder = relationship(
        "UserORM",
        foreign_keys=[responder_id],
        back_populates="responded_conversations",
    )
    announcement = relationship("AnnouncementORM", back_populates="conversation")
    notification = relationship(
        "NotificationORM",
        back_populates="conversation",
        cascade="all, delete-orphan",
        passive_deletes=True,
    )
