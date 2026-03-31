from uuid import UUID

from teamup.core import get_logger
from teamup.domain import (
    Announcement,
    Game,
    IAnnouncementRepository,
    User,
)
from teamup.schemas import (
    AnnouncementCreateIn,
    AnnouncementUpdateIn,
)

from ..exceptions import (
    AnnouncementCreationError,
    AnnouncementDeleteError,
    AnnouncementNotFoundError,
    AnnouncementUpdateError,
    GameNotFoundError,
    InvalidRankRangeError,
    PermissionDeniedError,
)

logger = get_logger()


class AnnouncementListingService:
    def __init__(self, ann_r: IAnnouncementRepository):
        logger.info("Инициализация AnnouncementListingService")
        self._ann_r = ann_r

    async def create_announcement(
        self, req: AnnouncementCreateIn, user_id: UUID
    ) -> Announcement:
        """
        Создать объявление. Выбрасывает исключения при ошибке.

        Args:
            `req`: Объект запроса с данными для создания объявления.
            `user_id`: id пользователя, создающего объявление.

        Returns:
            Объект созданного объявления.

        Raises:
            `InvalidRankRangeError`: Если значения требуемых рангов некорректны.
            `ForbiddenError`: Если пользователь не имеет прав на создание объявления.
            `PermissionDeniedError`: Если пользователь не имеет прав на создание объявления.
            `GameNotFoundError`: Если игра не найдена.
        """

        if not req.check_rank_range():
            logger.warning(f"Некорректный диапазон рангов в запросе от {user_id}.")
            raise InvalidRankRangeError("Некорректные значения требуемых рангов")

        logger.info(
            f"Пользователь {user_id} создаёт объявление для игры {req.game_id}."
        )

        new_announcement = Announcement.create(
            type=req.type,
            user_id=user_id,
            game_id=req.game_id,
            description=req.description,
            rank_min=req.rank_min,
            rank_max=req.rank_max,
        )

        announcement = await self._ann_r.create(new_announcement)
        if announcement is None:
            logger.error(f"Не удалось создать объявление для пользователя {user_id}.")
            raise AnnouncementCreationError("Не удалось создать объявление")

        return announcement

    async def get_active_announcements(
        self, user_id: UUID
    ) -> list[tuple[Announcement, User, Game]]:
        """
        Получить все активные объявления.

        Args:
            user_id: ID пользователя. Доступ к объявлвениям только авторизоавнными лицам.

        Returns:
            list[AnnouncementSummaryOut]: Список активных объявлений.
        """

        announcements = await self._ann_r.get_all_active_with_relations()
        logger.info(
            f"Получено {len(announcements)} активных объявлений для пользователя {user_id}."
        )
        return announcements

    async def get_announcement_by_id(
        self, announcement_id: UUID, user_id: UUID
    ) -> tuple[Announcement, User, Game]:
        """Получить объявление по ID.

        Args:
            `announcement_id`: ID объявления.
            `user_id`: ID пользователя. Доступ к объявлению только авторизованным лицам.

        Raises:
            `AnnouncementNotFoundError`: Если объявление не найдено.
            `PermissionDeniedError`: Если пользователь не имеет доступа к объявлению.
            `GameNotFoundError`: Если игра не найдена.
        """

        row = await self._ann_r.get_by_id_with_relations(announcement_id)
        if row is None:
            raise AnnouncementNotFoundError(
                f"Объявление с ID {announcement_id} не найдено"
            )

        a, u, g = row

        if u is None:
            raise PermissionDeniedError(
                f"Пользователь {user_id} не имеет доступа к объявлению"
            )
        if g is None:
            raise GameNotFoundError(f"Игра с ID {a.game_id} не найдена")

        logger.info(f"Объявление {announcement_id} получено пользователем {user_id}.")
        return a, u, g

    async def delete_announcement(self, announcement_id: UUID, user_id: UUID):
        """Удалить объявление. Возвращает None при успехе."""
        ann = await self._ann_r.get_by_id(announcement_id)
        if ann is None:
            logger.warning(f"Объявление с ID {announcement_id} не найдено.")
            raise AnnouncementNotFoundError(
                f"Объявление с ID {announcement_id} не найдено"
            )
        if not await self._ann_r.delete(ann):
            raise AnnouncementDeleteError("Некорректный запрос на удаление")
        logger.info(f"Объявление {announcement_id} удалено пользователем {user_id}.")

    async def update_announcement(
        self, req: AnnouncementUpdateIn, user_id: UUID
    ) -> tuple[Announcement, User, Game]:
        """
        Обновить объявление.

        Args:
            `req`: Объект запроса на обновление объявления.
            `user_id`: Идентификатор пользователя, который выполняет запрос.

        Returns:
            Объект ответа с обновленным объявлением.

        Raises:
            `AnnouncementUpdateError`: Если произошла ошибка при обновлении объявления.
            `AnnouncementNotFoundError`: Если объявление не найдено.
            `PermissionDeniedError`: Если пользователь не имеет прав на обновление объявления.
            `GameNotFoundError`: Если игра не найдена.
        """
        row = await self._ann_r.get_by_id_with_relations(req.announcement_id)
        if row is None:
            logger.error(f"Объявление {req.announcement_id} не найдено.")
            raise AnnouncementNotFoundError("Объявление не найдено")

        a, u, g = row

        a.type = req.type
        a.description = req.description
        a.rank_min = req.rank_min
        a.rank_max = req.rank_max
        a.status = req.status

        u_ann = await self._ann_r.update(a)
        if u_ann is None:
            logger.error(f"Не удалось обновить объявление {req.announcement_id}.")
            raise AnnouncementUpdateError("Не удалось обновить объявление")

        logger.info(
            f"Объявление {a.announcement_id} обновлено пользователем {user_id}."
        )

        return u_ann, u, g
