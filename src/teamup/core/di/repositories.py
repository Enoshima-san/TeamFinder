from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

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
from teamup.infra.database import get_async_session


async def get_user_repository(
    session: AsyncSession = Depends(get_async_session),
) -> IUserRepository:
    return UserRepository(session)


async def get_game_repository(
    session: AsyncSession = Depends(get_async_session),
) -> IGameRepository:
    return GameRepository(session)


async def get_user_games_repository(
    session: AsyncSession = Depends(get_async_session),
) -> IUserGamesRepository:
    return UserGamesRepository(session)


async def get_announcement_repository(
    session: AsyncSession = Depends(get_async_session),
) -> IAnnouncementRepository:
    return AnnouncementRepository(session)


async def get_response_repository(
    session: AsyncSession = Depends(get_async_session),
) -> IResponseRepository:
    return ResponseRepository(session)


async def get_conversation_repository(
    session: AsyncSession = Depends(get_async_session),
) -> IConversationRepository:
    return ConversationRepository(session)


async def get_message_repository(
    session: AsyncSession = Depends(get_async_session),
) -> IMessageRepository:
    return MessageRepository(session)


async def get_notification_repository(
    session: AsyncSession = Depends(get_async_session),
) -> INotificationRepository:
    return NotificationRepository(session)
