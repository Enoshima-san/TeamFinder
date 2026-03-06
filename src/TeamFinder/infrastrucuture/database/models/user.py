from datetime import datetime
from uuid import uuid4

from sqlalchemy import UUID, Boolean, Column, DateTime, Integer, String
from sqlalchemy.orm import relationship

from ....domain.enums import UserRole
from .base import Base


class User(Base):
    __tablename__ = "user"

    user_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    username = Column(String(255), unique=True, nullable=False)
    email = Column(String(255), unique=True, nullable=False)
    password_hash = Column(String(255), nullable=False)
    registration_date = Column(DateTime, default=datetime.now)
    last_login = Column(DateTime, default=datetime.now, onupdate=datetime.now)
    is_active = Column(Boolean, default=True)
    role = Column(String(255), nullable=False, default=UserRole.USER.value)
    has_microphone = Column(Boolean, default=False)
    age = Column(Integer)
    about_me = Column(String(255))
    is_blocked = Column(Boolean, default=False)
    blocked_reason = Column(String(255))

    user_games = relationship("UserGames", back_populates="user")
    raitings = relationship("PlayerRating", back_populates="user")
    responses = relationship("Response", back_populates="user")
    announcements = relationship("Announcement", back_populates="user")
    complaints = relationship("Complaints", back_populates="user")
