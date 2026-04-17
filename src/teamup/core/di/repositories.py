from teamup.domain import (
    IAnnouncementRepository,
    IConversationRepository,
    IGameRepository,
    IMessageRepository,
    INotificationRepository,
    IResponseRepository,
    IUserGamesRepository,
    IUserRepository,
)
from teamup.infra import (
    AnnouncementRepository,
    ConversationRepository,
    GameRepository,
    MessageRepository,
    NotificationRepository,
    ResponseRepository,
    UserGamesRepository,
    UserRepository,
)


async def get_user_repository(session) -> IUserRepository:
    return UserRepository(session)


async def get_game_repository(session) -> IGameRepository:
    return GameRepository(session)


async def get_user_games_repository(session) -> IUserGamesRepository:
    return UserGamesRepository(session)


async def get_announcement_repository(session) -> IAnnouncementRepository:
    return AnnouncementRepository(session)


async def get_response_repository(session) -> IResponseRepository:
    return ResponseRepository(session)


async def get_conversation_repository(session) -> IConversationRepository:
    return ConversationRepository(session)


async def get_message_repository(session) -> IMessageRepository:
    return MessageRepository(session)


async def get_notification_repository(session) -> INotificationRepository:
    return NotificationRepository(session)
