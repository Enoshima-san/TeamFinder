from uuid import UUID

from teamup.core import get_logger
from teamup.domain import IUserRepository, User

from ..exceptions import UserNotFoundError

logger = get_logger()


class FullUserInfoUseCase:
    def __init__(self, user_r: IUserRepository):
        logger.info("Инициализация FullUserInfoUseCase")
        self._user_r = user_r

    async def __call__(self, user_id: UUID) -> User:
        user = await self._user_r.get_by_id(user_id)
        if user is None:
            raise UserNotFoundError("Пользователь не найден")
        logger.info(f"Запрос на полную информаицю о пользователе {user.username}")
        return user
