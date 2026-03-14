from typing import cast
from uuid import UUID

from domain import Rank

from ..models import RankORM


class RankMapper:
    @staticmethod
    def to_domain(orm: RankORM | None) -> "Rank":
        if not orm:
            raise ValueError("RankORM is None")

        return Rank(
            rank_id=cast(UUID, orm.rank_id),
            game_id=cast(UUID, orm.game_id),
            rank_name=cast(str, orm.rank_name),
            rank_level=cast(int, orm.rank_level),
        )

    @staticmethod
    def to_orm(entity: Rank | None) -> "RankORM":
        if not entity:
            raise ValueError("Rank is None")

        return RankORM(
            rank_id=entity.rank_id,
            game_id=entity.game_id,
            rank_name=entity.rank_name,
            rank_level=entity.rank_level,
        )
