from uuid import UUID

from teamup.core import get_logger
from teamup.domain import Game, IGameRepository, IUserGamesRepository, UserGames

logger = get_logger()


class GetUserGamesUseCase:
    def __init__(self, ug_r: IUserGamesRepository, g_r: IGameRepository):
        logger.info("Инициализация GetUserGamesUseCase")
        self._ug_r = ug_r
        self._g_r = g_r

    async def _map_game(self, user_game: UserGames) -> Game | None:
        game = await self._g_r.get_by_id(user_game.game_id)
        return game

    async def __call__(self, user_id: UUID) -> list[Game]:
        user_games = await self._ug_r.get_all_by_user(user_id) or []

        games: list[Game] = []
        for ug in user_games:
            game = await self._g_r.get_by_id(ug.game_id)
            if game is not None:
                games.append(game)
        return games
