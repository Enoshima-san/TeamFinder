from datetime import datetime
from typing import cast
from uuid import UUID

from src.teamup.domain import PlayerRating

from ..models import PlayerRatingORM


class PlayerRatingMapper:
    @staticmethod
    def to_domain(orm: PlayerRatingORM | None) -> PlayerRating:
        if not orm:
            raise ValueError("ORM object is None")

        return PlayerRating(
            rating_id=cast(UUID, orm.rating_id),
            user_id=cast(UUID, orm.user_id),
            game_id=cast(UUID, orm.game_id),
            response_id=cast(UUID, orm.response_id),
            rating_value=cast(int, orm.rating_value),
            created_at=cast(datetime, orm.created_at),
        )

    @staticmethod
    def to_orm(entity: PlayerRating | None) -> PlayerRatingORM:
        if not entity:
            raise ValueError("Entity is None")

        return PlayerRatingORM(
            rating_id=entity.rating_id,
            user_id=entity.user_id,
            game_id=entity.game_id,
            response_id=entity.response_id,
            raiting_value=entity.rating_value,
            created_at=entity.created_at,
        )
