from uuid import UUID

from teamup.core import get_logger
from teamup.domain import (
    Announcement,
    Conversation,
    Game,
    IAnnouncementRepository,
    IConversationRepository,
    IGameRepository,
    IUserRepository,
    User,
)

from .exceptions import (
    AnnouncementNotFoundError,
    ConversationNotFoundError,
    GameNotFoundError,
    PermissionDeniedError,
    UnauthorizedError,
)

logger = get_logger()


class BaseRules:
    @staticmethod
    async def get_user_or_fail(user_r: IUserRepository, user_id: UUID) -> User:
        """Helper: получить пользователя или выбросить исключение"""
        user = await user_r.get_by_id_light(user_id)
        if user is None:
            logger.warning(f"Пользователь с ID {user_id} не найден.")
            raise UnauthorizedError(f"Пользователь с ID {user_id} не найден")
        return user

    @staticmethod
    async def get_game_or_fail(game_r: IGameRepository, game_id: UUID) -> Game:
        """Helper: получить игру или выбросить исключение"""
        game = await game_r.get_by_id(game_id)
        if game is None:
            logger.warning(f"Игра с ID {game_id} не найдена.")
            raise GameNotFoundError(f"Игра с ID {game_id} не найдена")
        return game

    @staticmethod
    async def get_announcement_or_fail(
        ann_r: IAnnouncementRepository, announcement_id: UUID
    ) -> Announcement:
        """Helper: получить объявление или выбросить исключение"""
        announcement = await ann_r.get_by_id(announcement_id)
        if announcement is None:
            logger.warning(f"Объявление с ID {announcement_id} не найдено.")
            raise AnnouncementNotFoundError(
                f"Объявление с ID {announcement_id} не найдено"
            )
        return announcement

    @staticmethod
    async def get_conversation_or_fail(
        conv_r: IConversationRepository, conversation_id: UUID
    ) -> Conversation:
        """Helper: получить диалог или выбросить исключение"""
        conversation = await conv_r.get_by_id(conversation_id)
        if conversation is None:
            logger.warning(f"Диалог с ID {conversation_id} не найден.")
            raise ConversationNotFoundError(f"Диалог с ID {conversation_id} не найден")
        return conversation

    @staticmethod
    async def check_ownership_or_admin(
        user_r: IUserRepository,
        ann_r: IAnnouncementRepository,
        announcement_id: UUID,
        user_id: UUID,
    ):
        """Helper: проверить, что пользователь владелец или админ"""
        user = await BaseRules.get_user_or_fail(user_r, user_id)
        if user.is_admin():
            return
        announcement = await BaseRules.get_announcement_or_fail(ann_r, announcement_id)
        if announcement.user_id != user_id:
            raise PermissionDeniedError("Нет прав на эту операцию")
