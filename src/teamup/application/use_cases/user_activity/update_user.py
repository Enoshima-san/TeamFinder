from uuid import UUID

from teamup.core import get_logger
from teamup.domain import IUserRepository
from teamup.schemas import UserUpdateRequest, UserUpdateResponse

from ...base_rules import BaseRules
from ...exceptions import UserNotFoundError


class UpdateUserUseCase:
    def __init__(self, user_r: IUserRepository):
        self.logger = get_logger()
        self._user_r = user_r

    async def __call__(
        self, req: UserUpdateRequest, user_id: UUID
    ) -> UserUpdateResponse:
        user = await BaseRules.get_user_or_fail(self._user_r, user_id)
        if req.username:
            user.set_username(req.username)
            self.logger.debug("Никнейм изменен")
        if req.about_me:
            user.set_about(req.about_me)
            self.logger.debug("Описание профиля изменено")
        res = await self._user_r.update(user)
        if res is None:
            raise UserNotFoundError(f"Пользователь с ID:{user_id} не найден")
        self.logger.info(f"Пользователь с ID:{user_id} успешно обновлен")
        return UserUpdateResponse(
            user_id=res.user_id, username=res.username, about_me=res.about_me
        )
