from uuid import UUID

from src.teamup.core import get_logger
from src.teamup.domain import (
    Announcement,
    Game,
    User,
)
from src.teamup.schemas import (
    AnnouncementCreateIn,
    AnnouncementOut,
    AnnouncementSummaryOut,
    AnnouncementUpdateIn,
    GameBriefDto,
    UserBriefDto,
)

from ..di import (
    get_announcement_repository,
    get_game_repository,
    get_user_repository,
)
from ..exceptions import (
    AnnouncementCreationError,
    AnnouncementDeleteError,
    AnnouncementNotFoundError,
    AnnouncementUpdateError,
    ForbiddenError,
    GameNotFoundError,
    InvalidRankRangeError,
    PermissionDeniedError,
)

logger = get_logger()


class AnnouncementListingService:
    def __init__(
        self,
    ):
        logger.info("Инициализация AnnouncementListingService")

    async def _get_user_or_fail(self, user_id: UUID) -> User:
        """Helper: получить пользователя или выбросить исключение"""
        async with await get_user_repository() as user_repository:
            user = await user_repository.get_by_id(user_id)
            if user is None:
                logger.warning(f"Пользователь с ID {user_id} не найден.")
                raise PermissionDeniedError(f"Пользователь с ID {user_id} не найден")
            return user

    async def _get_game_or_fail(self, game_id: UUID) -> Game:
        """Helper: получить игру или выбросить исключение"""
        async with await get_game_repository() as game_repository:
            game = await game_repository.get_by_id(game_id)
            if game is None:
                logger.warning(f"Игра с ID {game_id} не найдена.")
                raise GameNotFoundError(f"Игра с ID {game_id} не найдена")
            return game

    async def _get_announcement_or_fail(self, announcement_id: UUID) -> Announcement:
        """Helper: получить объявление или выбросить исключение"""
        async with await get_announcement_repository() as announcement_repository:
            announcement = await announcement_repository.get_by_id(announcement_id)
            if announcement is None:
                logger.warning(f"Объявление с ID {announcement_id} не найдено.")
                raise AnnouncementNotFoundError(
                    f"Объявление с ID {announcement_id} не найдено"
                )
            return announcement

    async def _check_ownership_or_admin(
        self, announcement: Announcement, user: User
    ) -> None:
        """Helper: проверить, что пользователь владелец или админ"""
        if announcement.user_id != user.user_id and not user.is_admin():
            logger.warning(
                f"Пользователь {user.user_id} не имеет прав на объявление {announcement.announcement_id}."
            )
            raise ForbiddenError("Нет прав на эту операцию")

    async def create_announcement(
        self, req: AnnouncementCreateIn, user_id: UUID
    ) -> AnnouncementOut:
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

        user = await self._get_user_or_fail(user_id)
        game = await self._get_game_or_fail(req.game_id)

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

        async with await get_announcement_repository() as announcement_repository:
            announcement = await announcement_repository.create(new_announcement)
            if announcement is None:
                logger.error(
                    f"Не удалось создать объявление для пользователя {user_id}."
                )
                raise AnnouncementCreationError("Не удалось создать объявление")

            logger.info(
                f"Объявление {announcement.announcement_id} успешно создано пользователем {user.user_id}."
            )

            return AnnouncementOut.create(announcement, user, game)

    async def get_active_announcements(
        self, user_id: UUID
    ) -> list[AnnouncementSummaryOut]:
        """
        Получить все активные объявления.

        Args:
            user_id: ID пользователя. Доступ к объявлвениям только авторизоавнными лицам.

        Returns:
            list[AnnouncementSummaryOut]: Список активных объявлений.
        """

        await self._get_user_or_fail(user_id)

        async with await get_announcement_repository() as announcement_repository:
            announcements = (
                await announcement_repository.get_all_active_with_relations()
            )

            response_list = [
                AnnouncementSummaryOut(
                    announcement_id=a.announcement_id,
                    type=a.type,
                    rank_max=a.rank_max,
                    rank_min=a.rank_min,
                    status=a.status,
                    user=UserBriefDto.from_user(u),
                    game=GameBriefDto.from_game(g),
                )
                for a, u, g in announcements
            ]

            logger.info(
                f"Получено {len(response_list)} активных объявлений для пользователя {user_id}."
            )
            return response_list

    async def get_announcement_by_id(
        self, announcement_id: UUID, user_id: UUID
    ) -> AnnouncementOut:
        """Получить объявление по ID.

        Args:
            `announcement_id`: ID объявления.
            `user_id`: ID пользователя. Доступ к объявлению только авторизованным лицам.

        Raises:
            `AnnouncementNotFoundError`: Если объявление не найдено.
            `PermissionDeniedError`: Если пользователь не имеет доступа к объявлению.
            `GameNotFoundError`: Если игра не найдена.
        """

        announcement = await self._get_announcement_or_fail(announcement_id)
        user = await self._get_user_or_fail(user_id)
        game = await self._get_game_or_fail(announcement.game_id)

        logger.info(f"Объявление {announcement_id} получено пользователем {user_id}.")
        return AnnouncementOut.create(announcement, user, game)

    async def delete_announcement(self, announcement_id: UUID, user_id: UUID) -> None:
        """Удалить объявление. Возвращает None при успехе."""

        announcement = await self._get_announcement_or_fail(announcement_id)
        user = await self._get_user_or_fail(user_id)

        async with await get_announcement_repository() as announcement_repository:
            await self._check_ownership_or_admin(announcement, user)

            if not await announcement_repository.delete(announcement):
                raise AnnouncementDeleteError("Некорректный запрос на удаление")
            logger.info(
                f"Объявление {announcement_id} удалено пользователем {user_id}."
            )

    async def update_announcement(
        self, req: AnnouncementUpdateIn, user_id: UUID
    ) -> AnnouncementOut:
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

        announcement = await self._get_announcement_or_fail(req.announcement_id)
        user = await self._get_user_or_fail(user_id)

        await self._check_ownership_or_admin(announcement, user)

        announcement.type = req.type
        announcement.description = req.description
        announcement.rank_min = req.rank_min
        announcement.rank_max = req.rank_max
        announcement.status = req.status

        async with await get_announcement_repository() as announcement_repository:
            updated_announcement = await announcement_repository.update(announcement)
            if updated_announcement is None:
                logger.error(f"Не удалось обновить объявление {req.announcement_id}.")
                raise AnnouncementUpdateError("Не удалось обновить объявление")

            game = await self._get_game_or_fail(updated_announcement.game_id)

            logger.info(
                f"Объявление {announcement.announcement_id} обновлено пользователем {user_id}."
            )
            return AnnouncementOut.create(updated_announcement, user, game)
