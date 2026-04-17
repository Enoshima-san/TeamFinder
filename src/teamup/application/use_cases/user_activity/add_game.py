from uuid import UUID

from teamup.core import get_logger
from teamup.domain import (
    IGameRepository,
    IUserGamesRepository,
    IUserRepository,
    UserGames,
)

from ...base_rules import BaseRules
from ...exceptions import UserGameCreationError

logger = get_logger()


class AddGameUseCase:
    def __init__(
        self,
        ug_r: IUserGamesRepository,
        user_r: IUserRepository,
        game_r: IGameRepository,
    ):
        logger.info("Инициализация AddGameUseCase")
        self._ug_r = ug_r
        self._user_r = user_r
        self._game_r = game_r

    async def __call__(self, user_id: UUID, game_id: UUID) -> UserGames:
        await BaseRules.get_user_or_fail(self._user_r, user_id)
        await BaseRules.get_game_or_fail(self._game_r, game_id)
        if self._check_owning(user_id, game_id):
            raise UserGameCreationError("Игра уже в библиотетеке пользователя.")
        ug = UserGames(user_id=user_id, game_id=game_id)
        user_game = await self._ug_r.create(ug)
        if user_game is None:
            raise UserGameCreationError("Невозможно добавить игру.")
        return user_game

    async def _check_owning(self, user_id: UUID, game_id: UUID) -> bool:
        exist_user_game = self._ug_r.get_by_fk(user_id, game_id)
        if exist_user_game:
            return True
        return False
