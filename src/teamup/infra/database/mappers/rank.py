from typing import Optional, cast
from uuid import UUID

from teamup.domain import Rank

from ..models import RankORM


class RankMapper:
    @staticmethod
    def to_domain(orm: Optional[RankORM]) -> Rank:
        if not orm:
            raise ValueError("RankORM is None")

        return Rank(
            rank_id=cast(UUID, orm.rank_id),
            game_id=cast(UUID, orm.game_id),
            rank_name=orm.rank_name,
            rank_level=orm.rank_level,
        )

    @staticmethod
    def to_orm(entity: Optional[Rank]) -> RankORM:
        if not entity:
            raise ValueError("Rank is None")

        return RankORM(
            rank_id=entity.rank_id,
            game_id=entity.game_id,
            rank_name=entity.rank_name,
            rank_level=entity.rank_level,
        )
