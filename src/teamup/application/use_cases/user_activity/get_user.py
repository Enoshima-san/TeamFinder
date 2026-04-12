from uuid import UUID

from teamup.application.exceptions import UserNotFoundError
from teamup.core import get_logger
from teamup.domain import IUserRepository, User

logger = get_logger()


class GetUserUseCase:
    def __init__(self, user_r: IUserRepository) -> None:
        self._user_r = user_r
        logger.info("Инициализация GetUserUseCase")

    async def __call__(self, user_c) -> User:
        user = None
        if self._is_id(user_c):
            user = await self._user_r.get_by_id_light(user_c)
            if user is not None:
                return user

        if self._is_email(user_c):
            user = await self._user_r.get_by_email(user_c)
            if user is not None:
                return user

        if self._is_username(user_c):
            user = await self._user_r.get_by_username(user_c)
            if user is not None:
                return user

        raise UserNotFoundError("Пользователь не найден")

    def _is_email(self, pn: str | UUID) -> bool:
        return isinstance(pn, str) and "@" in pn

    def _is_username(self, pn: str | UUID) -> bool:
        return isinstance(pn, str)

    def _is_id(self, pn: str | UUID) -> bool:
        return isinstance(pn, UUID)
