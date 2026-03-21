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
        self.session = async_session()
        logger.info("AnnouncementRepository проиницилизирован")

    async def create(self, announcement: Announcement) -> Optional[Announcement]:
        try:
            orm = AnnouncementMapper.to_orm(announcement)
            self.session.add(orm)
            await self.session.commit()
            await self.session.refresh(orm)
            return AnnouncementMapper.to_domain(orm)
        except IntegrityError as e:
            logger.error(f"Ошибка при создании объявления: {e}")
            await self.session.rollback()
            return None

    async def delete(self, announcement: Announcement) -> bool:
        delete_announcement = await self.session.get(
            AnnouncementORM, Announcement.announcement_id
        )
        if delete_announcement is None:
            return False

        await self.session.delete(delete_announcement)
        await self.session.commit()
        return True

    async def get_all(self) -> list[Announcement]:
        stmt = select(AnnouncementORM)
        result = await self.session.execute(stmt)
        announcements = result.scalars().all()

        return [AnnouncementMapper.to_domain(a) for a in announcements]

    async def get_by_id(self, announcement_id: UUID) -> Optional[Announcement]:
        announcement = await self.session.get(AnnouncementORM, announcement_id)
        if announcement is None:
            return None
        return AnnouncementMapper.to_domain(announcement)

    async def get_by_user(self, user: User) -> list[Announcement]:
        stmt = select(AnnouncementORM).where(AnnouncementORM.user_id == user.user_id)

        result = await self.session.execute(stmt)
        announcements = result.scalars().all()

        return [AnnouncementMapper.to_domain(a) for a in announcements]

    async def get_by_game(self, game: Game) -> list[Announcement]:
        stmt = select(AnnouncementORM).where(AnnouncementORM.game_id == game.game_id)

        result = await self.session.execute(stmt)
        announcements = result.scalars().all()

        return [AnnouncementMapper.to_domain(a) for a in announcements]

    async def get_all_active_with_relations(
        self,
    ) -> list[tuple[Announcement, User, Game]]:
        stmt = (
            select(AnnouncementORM, UserORM, GameORM)
            .join(UserORM, AnnouncementORM.user_id == UserORM.user_id)
            .join(GameORM, AnnouncementORM.game_id == GameORM.game_id)
            .where(AnnouncementORM.status == AnnouncementStatus.ACTIVE.value)
        )

        result = await self.session.execute(stmt)
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
        stmt = select(AnnouncementORM).where(
            AnnouncementORM.announcement_id == announcement.announcement_id
        )
        result = await self.session.execute(stmt)
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

        await self.session.commit()
        await self.session.refresh(orm)

        return AnnouncementMapper.to_domain(orm)
