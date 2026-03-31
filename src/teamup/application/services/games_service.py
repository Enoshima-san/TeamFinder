from uuid import UUID

from teamup.application.exceptions import GameNotFoundError
from teamup.core import get_logger
from teamup.domain import Game, IGameRepository

logger = get_logger()


class GamesService:
    def __init__(self, game_r: IGameRepository):
        logger.info("Инициализация GamesService")
        self._game_r = game_r

    async def get_all_games(self) -> list[Game]:
        games = await self._game_r.get_all()
        return games

    async def get_game_by_id(self, game_id: UUID) -> Game:
        game = await self._game_r.get_by_id(game_id)
        if game is None:
            logger.error(f"Игра с ID {game_id} не найдена")
            raise GameNotFoundError("Игра не найдена")

        return game
