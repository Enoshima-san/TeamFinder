from uuid import UUID

from teamup.application.exceptions import UserGameCreationError
from teamup.core import get_logger
from teamup.domain import IUserGamesRepository, UserGames

logger = get_logger()


class AddGameUseCase:
    def __init__(self, user_games_r: IUserGamesRepository):
        logger.info("Initializing AddGameUseCase")
        self._ug_r = user_games_r

    async def __call__(self, user_id: UUID, game_id: UUID) -> UserGames:
        ug = UserGames(user_id=user_id, game_id=game_id)
        user_game = await self._ug_r.create(ug)
        if user_game is None:
            raise UserGameCreationError("Невозможно добавить игру")
        return user_game
