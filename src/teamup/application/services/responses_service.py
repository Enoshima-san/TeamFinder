from uuid import UUID

from teamup.core import get_logger
from teamup.domain import IResponseRepository, Response

from ..exceptions import ResponseCreationError, ResponseDeletionError

logger = get_logger()


class ResponsesService:
    def __init__(self, res_r: IResponseRepository):
        logger.info("Инициализация ResponseService")
        self._res_r = res_r

    async def create_response(self, announcement_id: UUID, user_id: UUID) -> Response:
        _res = Response.create(user_id=user_id, announcement_id=announcement_id)

        res = await self._res_r.create(_res)
        if res is None:
            raise ResponseCreationError("Не удалось создать запрос")

        return res

    async def get_responses_by_announcement(
        self, announcement_id: UUID
    ) -> list[Response]:
        res = await self._res_r.get_by_announcement(announcement_id)
        return res

    async def delete_with_announcement(self, announcement_id: UUID):
        res = await self._res_r.get_by_announcement(announcement_id)
        results = [await self._res_r.delete(r) for r in res]
        if all(results):
            return True
        raise ResponseDeletionError("Не удалось удалить запросы, принадлежащие анонсу.")
