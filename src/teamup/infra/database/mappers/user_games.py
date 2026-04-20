from typing import Optional, cast
from uuid import UUID

from teamup.domain import UserGames

from ..models import UserGamesORM


class UserGamesMapper:
    @staticmethod
    def to_domain(orm: Optional[UserGamesORM]) -> UserGames:
        if not orm:
            raise ValueError("ORM object is None")

        return UserGames(
            user_id=cast(UUID, orm.user_id),
            game_id=cast(UUID, orm.game_id),
            preferred=orm.preferred,
        )

    @staticmethod
    def to_orm(entity: Optional[UserGames]) -> UserGamesORM:
        if not entity:
            raise ValueError("Entity is None")

        return UserGamesORM(
            user_id=entity.user_id,
            game_id=entity.game_id,
            preferred=entity.preferred,
        )
