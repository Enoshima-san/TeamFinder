from uuid import UUID

from teamup.core import get_logger
from teamup.domain import (
    IAnnouncementRepository,
    IResponseRepository,
    IUserRepository,
    Response,
)

from ..base_rules import BaseRules
from ..exceptions import ResponseCreationError

logger = get_logger()


class ResponsesService:
    def __init__(
        self,
        res_r: IResponseRepository,
        user_r: IUserRepository,
        ann_r: IAnnouncementRepository,
    ):
        logger.info("Инициализация ResponseService")
        self._res_r = res_r
        self._user_r = user_r
        self._ann_r = ann_r

    async def create_response(self, announcement_id: UUID, user_id: UUID) -> Response:
        await BaseRules.get_user_or_fail(self._user_r, user_id)
        await BaseRules.get_announcement_or_fail(self._ann_r, announcement_id)

        new_res = Response.create(user_id=user_id, announcement_id=announcement_id)
        res = await self._res_r.create(new_res)
        if res is None:
            raise ResponseCreationError("Не удалось создать запрос")

        return res

    async def get_responses_by_announcement(
        self, announcement_id: UUID
    ) -> list[Response]:
        await BaseRules.get_announcement_or_fail(self._ann_r, announcement_id)
        res = await self._res_r.get_by_announcement(announcement_id)
        return res
