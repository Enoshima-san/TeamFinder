from dataclasses import dataclass, field
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

    game_announcement: list["Announcement"] = field(default_factory=list)
    game_rank: list["Rank"] = field(default_factory=list)
    game_user_games: list["UserGames"] = field(default_factory=list)
    game_player_rating: list["PlayerRating"] = field(default_factory=list)

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
        game_icon: bytes,
    ) -> "Game":
        if len(game_name) < 3:
            raise ValueError("Название игры должно быть больше 3 символов")
        if len(game_name) > 50:
            raise ValueError("Название игры не может быть больше 50 символов")
        if not game_icon:
            raise ValueError("Логотип игры не может быть пустой")
        return Game(game_name=game_name, game_icon=game_icon)
