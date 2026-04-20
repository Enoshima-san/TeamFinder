from typing import Optional, cast
from uuid import UUID

from teamup.domain import Game

from ..models import GameORM
from ._map_relation import _map_relation
from .announcement import AnnouncementMapper
from .player_rating import PlayerRatingMapper
from .rank import RankMapper
from .user_games import UserGamesMapper


class GameMapper:
    @staticmethod
    def to_domain(orm: Optional[GameORM]) -> Game:
        if not orm:
            raise ValueError("ORM object is None")

        user_games = _map_relation(orm, "user_games", UserGamesMapper.to_domain)
        announcement = _map_relation(orm, "announcement", AnnouncementMapper.to_domain)
        rank = _map_relation(orm, "rank", RankMapper.to_domain)
        player_rating = _map_relation(
            orm, "player_rating", PlayerRatingMapper.to_domain
        )

        return Game(
            game_id=cast(UUID, orm.game_id),
            game_name=orm.game_name,
            game_icon=orm.game_icon,
            game_user_games=user_games,
            game_announcement=announcement,
            game_rank=rank,
            game_player_rating=player_rating,
        )

    @staticmethod
    def to_orm(entity: Optional[Game]) -> GameORM:
        if not entity:
            raise ValueError("Entity is None")

        return GameORM(
            game_id=entity.game_id,
            game_name=entity.game_name,
            game_icon=entity.game_icon,
        )
