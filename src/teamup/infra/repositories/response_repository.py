from typing import Optional
from uuid import UUID

from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from teamup.core import get_logger
from teamup.domain import IResponseRepository, Response

from ..database import ResponseMapper, ResponseORM

logger = get_logger()


class ResponseRepository(IResponseRepository):
    def __init__(self, session: AsyncSession):
        self.session = session
        logger.info("Инициализация ResponseRepository")

    async def create(self, response: Response) -> Optional[Response]:
        try:
            orm = ResponseMapper.to_orm(response)
            self.session.add(orm)
            await self.session.flush()
            await self.session.refresh(orm)
            return ResponseMapper.to_domain(orm)
        except IntegrityError as e:
            logger.error(f"Ошибка при создании ответа: {e}")
            await self.session.rollback()
            return None

    async def delete(self, response: Response) -> bool:
        del_response = await self.session.get(ResponseORM, response.response_id)
        if del_response is None:
            logger.error(f"Ответ с ID {response.response_id} не найден")
            return False

        await self.session.delete(del_response)
        await self.session.flush()
        logger.info(f"Ответ с ID {response.response_id} успешно удален")
        return True

    async def update(self, response: Response) -> Optional[Response]:
        update_response = await self.session.get(ResponseORM, response.response_id)
        if update_response is None:
            logger.error(f"Ответ с ID {response.response_id} не найден")
            return None

        update_response.status = response.status
        await self.session.flush()
        await self.session.refresh(update_response)
        logger.info(f"Ответ с ID {response.response_id} успешно обновлен")
        return ResponseMapper.to_domain(update_response)

    async def get_by_user(self, user_id: UUID) -> list[Response]:
        stmt = select(ResponseORM).where(ResponseORM.user_id == user_id)
        result = await self.session.execute(stmt)
        return [ResponseMapper.to_domain(row) for row in result.scalars().all()]

    async def get_by_announcement(self, announcement_id: UUID) -> list[Response]:
        stmt = select(ResponseORM).where(ResponseORM.announcement_id == announcement_id)
        result = await self.session.execute(stmt)
        return [ResponseMapper.to_domain(row) for row in result.scalars().all()]
