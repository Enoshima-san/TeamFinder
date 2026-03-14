from dataclasses import dataclass, field
from typing import List
from uuid import UUID, uuid4

from .announcement import Announcement
from .player_rating import PlayerRating
from .rank import Rank
from .user_games import UserGames


@dataclass
class Game:
    game_name: str
    game_icon: bytes
    game_id: UUID = field(default_factory=uuid4)

    announcement: List["Announcement"] = field(default_factory=list)
    rank: List["Rank"] = field(default_factory=list)
    user_games: List["UserGames"] = field(default_factory=list)
    player_rating: List["PlayerRating"] = field(default_factory=list)

    def set_game_name(self, game_name: str):
        """Устанавливает название игры"""
        if len(game_name) < 3:
            raise ValueError("Название игры должно быть больше 3 символов")
        if len(game_name) > 50:
            raise ValueError("Название игры не может быть больше 50 символов")
        self.game_name = game_name

    def set_icon(self, icon: bytes):
        """Устанавливает логотип игры"""
        if not icon:
            raise ValueError("Логотип игры не может быть пустой")
        self.game_icon = icon

    @staticmethod
    def create(
        game_name: str,
        icon: bytes,
    ) -> "Game":
        if len(game_name) < 3:
            raise ValueError("Название игры должно быть больше 3 символов")
        if len(game_name) > 50:
            raise ValueError("Название игры не может быть больше 50 символов")
        if not icon:
            raise ValueError("Логотип игры не может быть пустой")
        return Game(game_name=game_name, game_icon=icon)
