from datetime import datetime
from typing import Optional
from uuid import UUID

from sqlalchemy import select
from sqlalchemy.exc import IntegrityError

from src.teamup.core import get_logger
from src.teamup.domain import (
    Announcement,
    AnnouncementStatus,
    Game,
    IAnnouncementRepository,
    User,
)

from ..database import (
    AnnouncementMapper,
    AnnouncementORM,
    GameMapper,
    GameORM,
    UserMapper,
    UserORM,
    async_session,
)

logger = get_logger()


class AnnouncementRepository(IAnnouncementRepository):
    def __init__(self):
        super().__init__()
        logger.info("AnnouncementRepository проиницилизирован")

    async def __aenter__(self):
        self.session = async_session()
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        return await super().__aexit__(exc_type, exc_val, exc_tb)

    async def close(self):
        if self.session:
            await self.session.close()
            self.session = None

    async def create(self, announcement: Announcement) -> Optional[Announcement]:
        self.check_session()
        try:
            orm = AnnouncementMapper.to_orm(announcement)
            self.session.add(orm)  # type: ignore[reportOptionalMemberAccess]
            await self.session.commit()  # type: ignore[reportOptionalMemberAccess]
            await self.session.refresh(orm)  # type: ignore[reportOptionalMemberAccess]
            return AnnouncementMapper.to_domain(orm)
        except IntegrityError as e:
            logger.error(f"Ошибка при создании объявления: {e}")
            await self.session.rollback()  # type: ignore[reportOptionalMemberAccess]
            return None

    async def delete(self, announcement: Announcement) -> bool:
        self.check_session()
        delete_announcement = await self.session.get(  # type: ignore[reportOptionalMemberAccess]
            AnnouncementORM, announcement.announcement_id
        )
        if delete_announcement is None:
            logger.error(f"Объявление с ID {announcement.announcement_id} не найдено")
            return False

        await self.session.delete(delete_announcement)  # type: ignore[reportOptionalMemberAccess]
        await self.session.commit()  # type: ignore[reportOptionalMemberAccess]
        logger.info(f"Объявление с ID {announcement.announcement_id} успешно удалено")
        return True

    async def get_all(self) -> list[Announcement]:
        self.check_session()
        stmt = select(AnnouncementORM)
        result = await self.session.execute(stmt)  # type: ignore[reportOptionalMemberAccess]
        announcements = result.scalars().all()

        return [AnnouncementMapper.to_domain(a) for a in announcements]

    async def get_by_id(self, announcement_id: UUID) -> Optional[Announcement]:
        announcement = await self.session.get(AnnouncementORM, announcement_id)  # type: ignore[reportOptionalMemberAccess]
        if announcement is None:
            return None
        return AnnouncementMapper.to_domain(announcement)

    async def get_by_user(self, user: User) -> list[Announcement]:
        self.check_session()
        stmt = select(AnnouncementORM).where(AnnouncementORM.user_id == user.user_id)

        result = await self.session.execute(stmt)  # type: ignore[reportOptionalMemberAccess]
        announcements = result.scalars().all()

        return [AnnouncementMapper.to_domain(a) for a in announcements]

    async def get_by_game(self, game: Game) -> list[Announcement]:
        self.check_session()
        stmt = select(AnnouncementORM).where(AnnouncementORM.game_id == game.game_id)

        result = await self.session.execute(stmt)  # type: ignore[reportOptionalMemberAccess]
        announcements = result.scalars().all()

        return [AnnouncementMapper.to_domain(a) for a in announcements]

    async def get_all_active_with_relations(
        self,
    ) -> list[tuple[Announcement, User, Game]]:
        self.check_session()
        stmt = (
            select(AnnouncementORM, UserORM, GameORM)
            .join(UserORM, AnnouncementORM.user_id == UserORM.user_id)
            .join(GameORM, AnnouncementORM.game_id == GameORM.game_id)
            .where(AnnouncementORM.status == AnnouncementStatus.ACTIVE.value)
        )

        result = await self.session.execute(stmt)  # type: ignore[reportOptionalMemberAccess]
        announcements = result.all()

        return [
            (
                AnnouncementMapper.to_domain(a),
                UserMapper.to_domain(u),
                GameMapper.to_domain(g),
            )
            for a, u, g in announcements
        ]

    async def update(self, announcement: Announcement) -> Optional[Announcement]:
        self.check_session()
        stmt = select(AnnouncementORM).where(
            AnnouncementORM.announcement_id == announcement.announcement_id
        )
        result = await self.session.execute(stmt)  # type: ignore[reportOptionalMemberAccess]
        orm = result.scalar()

        if orm is None:
            logger.error(f"Объявление с id {announcement.announcement_id} не найдено")
            return None

        orm.type = announcement.type
        orm.rank_min = announcement.rank_min
        orm.rank_max = announcement.rank_max
        orm.description = orm.description
        orm.status = orm.status
        orm.updated_at = datetime.now()

        await self.session.commit()  # type: ignore[reportOptionalMemberAccess]
        await self.session.refresh(orm)  # type: ignore[reportOptionalMemberAccess]

        return AnnouncementMapper.to_domain(orm)
