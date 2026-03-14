from uuid import uuid4

from sqlalchemy import UUID, Boolean, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import Base


class UserGamesORM(Base):
    __tablename__ = "user_games"

    user_game_id: Mapped[UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid4
    )
    game_id: Mapped[UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("game.game_id"), nullable=False
    )
    user_id: Mapped[UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("user.user_id"), nullable=False
    )
    preferred: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)

    user = relationship("UserORM", back_populates="user_games")
    game = relationship("GameORM", back_populates="user_games")
