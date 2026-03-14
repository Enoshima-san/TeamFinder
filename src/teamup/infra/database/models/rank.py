from uuid import uuid4

from sqlalchemy import UUID, ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import Base


class RankORM(Base):
    __tablename__ = "rank"

    rank_id: Mapped[UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid4
    )
    game_id: Mapped[UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("game.game_id"), nullable=False
    )
    rank_level: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    rank_name: Mapped[str] = mapped_column(String(100), nullable=False)

    game = relationship("GameORM", back_populates="rank")
