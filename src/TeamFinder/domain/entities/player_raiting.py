from dataclasses import dataclass, field
from datetime import datetime
from uuid import UUID, uuid4

from ..enums import PlayersBehavior


@dataclass
class PlayerRating:
    user_id: UUID
    game_id: UUID
    response_id: UUID
    raiting_id: UUID = field(default_factory=uuid4)

    rating_value: int = PlayersBehavior.MAX_RATING.value
    created_at: datetime = field(default_factory=datetime.now)

    def set_rating(self, rating_value: int):
        """Устанавливает рейтинг игрока"""
        if rating_value < PlayersBehavior.MIN_RATING.value:
            raise ValueError("Значение рейтинга не может быть меньше минимального")
        if rating_value > PlayersBehavior.MAX_RATING.value:
            raise ValueError("Значение рейтинга не может быть больше максимального")
        self.rating_value = rating_value

    @staticmethod
    def create(
        user_id: UUID, game_id: UUID, response_id: UUID, rating_value: int = 50
    ) -> "PlayerRating":
        if rating_value < PlayersBehavior.MIN_RATING.value:
            raise ValueError("Значение рейтинга не может быть меньше минимального")
        if rating_value > PlayersBehavior.MAX_RATING.value:
            raise ValueError("Значение рейтинга не может быть больше максимального")
        return PlayerRating(user_id, game_id, response_id, rating_value=rating_value)
