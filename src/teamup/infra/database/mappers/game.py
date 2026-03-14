from typing import cast
from uuid import UUID

from domain import Game
from rank import RankMapper

from ..models import GameORM
from ._map_relation import _map_relation
from .announcement import AnnouncementMapper
from .player_rating import PlayerRatingMapper
from .user_games import UserGamesMapper


class GameMapper:
    @staticmethod
    def to_domain(orm: GameORM | None) -> "Game":
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
            game_name=cast(str, orm.game_name),
            game_icon=cast(bytes, orm.game_icon),
            user_games=user_games,
            announcement=announcement,
            rank=rank,
            player_rating=player_rating,
        )

    @staticmethod
    def to_orm(entity: Game | None) -> "GameORM":
        if not entity:
            raise ValueError("Entity is None")

        return GameORM(
            game_id=entity.game_id,
            game_name=entity.game_name,
            game_icon=entity.game_icon,
        )
