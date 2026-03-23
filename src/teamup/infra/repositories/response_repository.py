from typing import Optional
from uuid import UUID

from sqlalchemy import select
from sqlalchemy.exc import IntegrityError

from src.teamup.core import get_logger
from src.teamup.domain import IResponseRepository, Response

from ..database import ResponseMapper, ResponseORM, async_session

logger = get_logger()


class ResponseRepository(IResponseRepository):
    def __init__(self):
        super().__init__()
        logger.info("ResponseRepository проинициализирован")

    async def __aenter__(self):
        self.session = async_session()
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await super().__aexit__(exc_type, exc_val, exc_tb)

    async def close(self):
        if self.session:
            await self.session.close()
            self.session = None

    async def create(self, response: Response) -> Optional[Response]:
        self.check_session()
        try:
            orm = ResponseMapper.to_orm(response)
            self.session.add(orm)  # type: ignore[reportOptionalMemberAccess]
            await self.session.commit()  # type: ignore[reportOptionalMemberAccess]
            await self.session.refresh(orm)  # type: ignore[reportOptionalMemberAccess]
            return ResponseMapper.to_domain(orm)  # type: ignore[reportOptionalMemberAccess]
        except IntegrityError as e:
            logger.error(f"Ошибка при создании ответа: {e}")
            await self.session.rollback()  # type: ignore[reportOptionalMemberAccess]
            return None

    async def delete(self, response: Response) -> bool:
        self.check_session()

        del_response = await self.session.get(  # type: ignore[reportOptionalMemberAccess]
            ResponseORM, response.response_id
        )
        if del_response is None:
            logger.error(f"Ответ с ID {response.response_id} не найден")
            return False

        self.session.delete(del_response)  # type: ignore[reportOptionalMemberAccess]
        await self.session.commit()  # type: ignore[reportOptionalMemberAccess]
        logger.info(f"Ответ с ID {response.response_id} успешно удален")
        return True

    async def update(self, response: Response) -> Optional[Response]:
        self.check_session()

        update_response = await self.session.get(  # type: ignore[reportOptionalMemberAccess]
            ResponseORM, response.response_id
        )
        if update_response is None:
            logger.error(f"Ответ с ID {response.response_id} не найден")
            return None

        update_response.status = response.status
        await self.session.commit()  # type: ignore[reportOptionalMemberAccess]
        await self.session.refresh(update_response)  # type: ignore[reportOptionalMemberAccess]
        logger.info(f"Ответ с ID {response.response_id} успешно обновлен")
        return ResponseMapper.to_domain(update_response)  # type: ignore[reportOptionalMemberAccess]

    async def get_by_user(self, user_id: UUID) -> list[Response]:
        self.check_session()

        stmt = select(ResponseORM).where(ResponseORM.user_id == user_id)
        result = await self.session.execute(stmt)  # type: ignore[reportOptionalMemberAccess]
        return [ResponseMapper.to_domain(row) for row in result.scalars().all()]

    async def get_by_announcement(self, announcement_id: UUID) -> list[Response]:
        self.check_session()

        stmt = select(ResponseORM).where(ResponseORM.announcement_id == announcement_id)
        result = await self.session.execute(stmt)  # type: ignore[reportOptionalMemberAccess]
        return [ResponseMapper.to_domain(row) for row in result.scalars().all()]
