from datetime import datetime
from typing import Optional
from uuid import UUID

from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from teamup.domain import (
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
)


class AnnouncementRepository(IAnnouncementRepository):
    def __init__(self, session: AsyncSession):
        super().__init__(session)
        self.logger.info("Инициализация AnnouncementRepository")

    async def create(self, announcement: Announcement) -> Optional[Announcement]:
        try:
            if announcement.game_ids:
                games_stmt = select(GameORM).where(
                    GameORM.game_id.in_(announcement.game_ids)
                )
                games_result = await self.session.execute(games_stmt)
                games_orm = list(games_result.scalars().all())

                if len(games_orm) != len(announcement.game_ids):
                    self.logger.warning(
                        f"Не все игры найдены: ожидалось {len(announcement.game_ids)}, "
                        f"найдено {len(games_orm)}"
                    )
            else:
                games_orm = []

            orm = AnnouncementMapper.to_orm(announcement)
            orm.games = games_orm

            self.session.add(orm)
            await self.session.flush()
            await self.session.refresh(orm)
            self.logger.info("Объявление сохранено в сессии.")

            return AnnouncementMapper.to_domain(orm)
        except IntegrityError as e:
            self.logger.error(f"Ошибка при создании объявления: {e}")
            await self.session.rollback()
            return None

    async def delete(self, announcement_id: UUID) -> bool:
        stmt = (
            select(AnnouncementORM)
            .options(selectinload(AnnouncementORM.games))
            .where(AnnouncementORM.announcement_id == announcement_id)
        )

        result = await self.session.execute(stmt)
        del_announcement = result.scalar_one_or_none()

        if del_announcement is None:
            self.logger.error(f"Объявление с ID:{announcement_id} не найдено.")
            return False

        await self.session.delete(del_announcement)
        await self.session.flush()
        self.logger.info(f"Объявление с ID:{announcement_id} удалено из сессии.")
        return True

    async def get_all(self) -> list[Announcement]:
        stmt = select(AnnouncementORM).options(selectinload(AnnouncementORM.games))
        result = await self.session.execute(stmt)
        announcements = result.scalars().unique().all()
        self.logger.info("Запрос на все объявления.")
        return [AnnouncementMapper.to_domain(a) for a in announcements]

    async def get_by_id(self, announcement_id: UUID) -> Optional[Announcement]:
        stmt = (
            select(AnnouncementORM)
            .options(selectinload(AnnouncementORM.games))
            .where(AnnouncementORM.announcement_id == announcement_id)
        )

        result = await self.session.execute(stmt)
        announcement = result.scalars().unique().one_or_none()

        if announcement is None:
            return None
        self.logger.info(f"Запрос на объявление с ID:{announcement_id}.")
        return AnnouncementMapper.to_domain(announcement)

    async def get_by_user(self, user: User) -> list[Announcement]:
        stmt = (
            select(AnnouncementORM)
            .options(selectinload(AnnouncementORM.games))
            .where(AnnouncementORM.user_id == user.user_id)
        )

        result = await self.session.execute(stmt)
        announcements = result.scalars().unique().all()
        self.logger.info(f"Запрос на объявления пользователя с ID:{user.user_id}.")
        return [AnnouncementMapper.to_domain(a) for a in announcements]

    async def get_by_game(self, game: Game) -> list[Announcement]:
        stmt = (
            select(AnnouncementORM)
            .options(selectinload(AnnouncementORM.games))
            .join(AnnouncementORM.games)
            .where(GameORM.game_id == game.game_id)
        )
        result = await self.session.execute(stmt)
        announcements = result.scalars().unique().all()
        self.logger.info(f"Запрос на объявления игры с ID:{game.game_id}.")
        return [AnnouncementMapper.to_domain(a) for a in announcements]

    async def get_all_active_with_relations(
        self,
    ) -> list[tuple[Announcement, User, list[Game]]]:
        stmt = (
            select(AnnouncementORM, UserORM, GameORM)
            .join(UserORM, AnnouncementORM.user_id == UserORM.user_id)
            .join(AnnouncementORM.games)
            .where(AnnouncementORM.status == AnnouncementStatus.ACTIVE.value)
        )
        result = await self.session.execute(stmt)
        rows = result.all()

        grouped: dict[UUID, tuple[Announcement, User, list[Game]]] = {}
        for a_orm, u_orm, g_orm in rows:
            ann_id = a_orm.announcement_id
            if ann_id not in grouped:
                grouped[ann_id] = (
                    AnnouncementMapper.to_domain(a_orm),
                    UserMapper.to_domain(u_orm),
                    [],
                )
            grouped[ann_id][2].append(GameMapper.to_domain(g_orm))

        self.logger.info("Запрос на все активные объявления со связями.")
        return list(grouped.values())

    async def get_by_id_with_relations(
        self, announcement_id: UUID
    ) -> Optional[tuple[Announcement, User, list[Game]]]:
        stmt = (
            select(AnnouncementORM, UserORM, GameORM)
            .join(UserORM, AnnouncementORM.user_id == UserORM.user_id)
            .join(AnnouncementORM.games)
            .where(AnnouncementORM.announcement_id == announcement_id)
        )
        result = await self.session.execute(stmt)
        rows = result.all()
        if not rows:
            return None
        a_orm, u_orm, _ = rows[0]
        games = [GameMapper.to_domain(g_orm) for _, _, g_orm in rows]
        self.logger.info(f"Запрос на объявление с ID:{announcement_id} со связями.")
        return (AnnouncementMapper.to_domain(a_orm), UserMapper.to_domain(u_orm), games)

    async def update(self, announcement: Announcement) -> Optional[Announcement]:
        stmt = (
            select(AnnouncementORM)
            .options(selectinload(AnnouncementORM.games))
            .where(AnnouncementORM.announcement_id == announcement.announcement_id)
        )
        result = await self.session.execute(stmt)
        orm = result.scalar_one_or_none()

        if orm is None:
            self.logger.error(
                f"Объявление с id {announcement.announcement_id} не найдено"
            )
            return None
        orm.type = announcement.type
        orm.rank_min = announcement.rank_min
        orm.rank_max = announcement.rank_max
        orm.description = announcement.description
        orm.status = announcement.status
        orm.has_microphone = announcement.has_microphone
        orm.updated_at = datetime.now()

        if announcement.game_ids:
            games_stmt = select(GameORM).where(
                GameORM.game_id.in_(announcement.game_ids)
            )
            games_result = await self.session.execute(games_stmt)
            orm.games = list(games_result.scalars().all())
        await self.session.flush()
        await self.session.refresh(orm)
        self.logger.info(
            f"Объявление с ID:{announcement.announcement_id} успешно обновлено в сессии."
        )
        return AnnouncementMapper.to_domain(orm)
