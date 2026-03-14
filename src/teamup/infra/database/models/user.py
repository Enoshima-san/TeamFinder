from datetime import datetime
from typing import Optional
from uuid import uuid4

from sqlalchemy import UUID, Boolean, DateTime, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.teamup.domain import UserRole

from .base import Base


class UserORM(Base):
    __tablename__ = "user"

    user_id: Mapped[UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid4
    )
    username: Mapped[str] = mapped_column(String(15), unique=True, nullable=False)
    email: Mapped[str] = mapped_column(String(255), unique=True, nullable=False)
    password_hash: Mapped[str] = mapped_column(String(255), nullable=False)
    registration_date: Mapped[datetime] = mapped_column(DateTime, default=datetime.now)
    last_login: Mapped[datetime] = mapped_column(
        DateTime, default=datetime.now, onupdate=datetime.now
    )
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
    role: Mapped[str] = mapped_column(
        String(15), nullable=False, default=UserRole.USER.value
    )
    has_microphone: Mapped[bool] = mapped_column(Boolean, default=False)
    age: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    about_me: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    is_blocked: Mapped[bool] = mapped_column(Boolean, default=False)
    blocked_reason: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)

    user_games = relationship("UserGamesORM", back_populates="user")
    player_rating = relationship("PlayerRatingORM", back_populates="user")
    response = relationship("ResponseORM", back_populates="user")
    announcement = relationship("AnnouncementORM", back_populates="user")
    complaints = relationship("ComplaintsORM", back_populates="user")
