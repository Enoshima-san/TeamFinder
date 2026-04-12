from uuid import UUID

from sqlalchemy.ext.asyncio import AsyncSession

from teamup.api.di.repositories import (
    get_announcement_repository,
    get_game_repository,
    get_user_repository,
)
from teamup.core import get_logger
from teamup.domain import Announcement, Game, User

from .exceptions import (
    AnnouncementNotFoundError,
    GameNotFoundError,
    PermissionDeniedError,
    UnauthorizedError,
)

logger = get_logger()


async def get_user_or_fail(session: AsyncSession, user_id: UUID) -> User:
    """Helper: получить пользователя или выбросить исключение"""
    user_r = await get_user_repository(session)
    user = await user_r.get_by_id_light(user_id)
    if user is None:
        logger.warning(f"Пользователь с ID {user_id} не найден.")
        raise UnauthorizedError(f"Пользователь с ID {user_id} не найден")
    return user


async def get_game_or_fail(session, game_id: UUID) -> Game:
    """Helper: получить игру или выбросить исключение"""
    game_r = await get_game_repository(session)
    game = await game_r.get_by_id(game_id)
    if game is None:
        logger.warning(f"Игра с ID {game_id} не найдена.")
        raise GameNotFoundError(f"Игра с ID {game_id} не найдена")
    return game


async def get_announcement_or_fail(session, announcement_id: UUID) -> Announcement:
    """Helper: получить объявление или выбросить исключение"""
    ann_r = await get_announcement_repository(session)
    announcement = await ann_r.get_by_id(announcement_id)
    if announcement is None:
        logger.warning(f"Объявление с ID {announcement_id} не найдено.")
        raise AnnouncementNotFoundError(f"Объявление с ID {announcement_id} не найдено")
    return announcement


async def check_ownership_or_admin(session, announcement_id: UUID, user_id: UUID):
    """Helper: проверить, что пользователь владелец или админ"""
    user = await get_user_or_fail(session, user_id)
    if user.is_admin:
        return
    announcement = await get_announcement_or_fail(session, announcement_id)
    if announcement.user_id != user_id:
        raise PermissionDeniedError("Нет прав на эту операцию")
